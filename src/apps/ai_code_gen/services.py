import io
import zipfile
from uuid import UUID

from loguru import logger

from src.apps.ai_code_gen.dependencies.repositories_dependencies import AICodeGenRepositoryDI
from src.apps.ai_code_gen.dto import (
    AICodeGenSessionCreateDTO,
    AICodeGenMessageCreateDTO,
    AICodeGenSessionWithMessagesReadDTO,
)
from src.apps.ai_code_gen.llm_response import LLMResponse
from src.apps.ai_code_gen.errors import (
    AICodeGenMessagesLimitExceededError,
    AICodeGenInvalidResponseError,
    AICodeGenNoAssistantMessageError,
)
from src.apps.ai_code_gen.enums import AICodeGenSessionStatus, AICodeGenRole
from src.apps.ai_code_gen.prompts import SYSTEM_PROMPT
from src.apps.ai_code_gen.validators import validate_user_prompt, validate_session_and_ownership
from src.core.config import settings, BOT_TEMPLATES_DIR
from src.infrastructure.llm.cli.openai import AsyncOpenAICli
from src.infrastructure.llm.enums import LLMChatMemberRole
from src.infrastructure.llm.types import LLMChatMessage


class AICodeGenService:
    def __init__(
        self,
        ai_code_gen_repository: AICodeGenRepositoryDI,
    ):
        self._ai_code_gen_repository = ai_code_gen_repository
        self._client = AsyncOpenAICli(model=settings.OPENAI_MODEL)

    async def create_session(self, user_id: UUID, prompt: str) -> AICodeGenSessionWithMessagesReadDTO:
        validate_user_prompt(prompt)
        session = await self._ai_code_gen_repository.create_session(
            AICodeGenSessionCreateDTO(
                user_id=user_id,
                status=AICodeGenSessionStatus.QUEUED,
            )
        )
        await self._ai_code_gen_repository.add_message(
            AICodeGenMessageCreateDTO(
                session_id=session.session_id,
                role=AICodeGenRole.USER,
                content=prompt,
                meta=None,
            )
        )
        await self._generate_and_store_response(session_id=session.session_id)
        return await self.get_session_with_messages(user_id=user_id, session_id=session.session_id)

    async def add_message(self, user_id: UUID, session_id: int, prompt: str) -> AICodeGenSessionWithMessagesReadDTO:
        validate_user_prompt(prompt)

        session = await self._ai_code_gen_repository.get_session_with_messages(session_id)
        validate_session_and_ownership(session=session, user_id=user_id)

        messages_count = await self._ai_code_gen_repository.count_messages(session_id)
        if messages_count >= settings.AI_CODEGEN_MAX_MESSAGES_PER_SESSION:
            raise AICodeGenMessagesLimitExceededError

        await self._ai_code_gen_repository.add_message(
            AICodeGenMessageCreateDTO(
                session_id=session_id,
                role=AICodeGenRole.USER,
                content=prompt,
                meta=None,
            )
        )
        await self._generate_and_store_response(session_id=session_id)
        return await self.get_session_with_messages(user_id=user_id, session_id=session_id)

    async def get_session_with_messages(self, user_id: UUID, session_id: int) -> AICodeGenSessionWithMessagesReadDTO:
        session = await self._ai_code_gen_repository.get_session_with_messages(session_id)
        validate_session_and_ownership(session=session, user_id=user_id)
        return session

    async def get_zip(self, user_id: UUID, session_id: int) -> io.BytesIO:
        session = await self._ai_code_gen_repository.get_session(session_id)
        validate_session_and_ownership(session=session, user_id=user_id)

        last_message = await self._ai_code_gen_repository.get_latest_assistant_message(session_id)
        if last_message is None or not last_message.meta:
            raise AICodeGenNoAssistantMessageError

        zip_data = io.BytesIO()
        with zipfile.ZipFile(zip_data, mode='w') as zipf:
            zipf.writestr('main.py', last_message.meta['code'])
            zipf.writestr('requirements.txt', '\n'.join(last_message.meta['requirements']))
            zipf.write(BOT_TEMPLATES_DIR / 'Dockerfile', 'Dockerfile')
        zip_data.seek(0)
        return zip_data

    async def _generate_and_store_response(self, session_id: int) -> None:
        await self._ai_code_gen_repository.update_session_status(
            session_id=session_id,
            status=AICodeGenSessionStatus.RUNNING,
        )
        messages_for_llm = await self._build_llm_messages(session_id)

        try:
            response = await self._client.make_structured_request(
                object_type=LLMResponse,
                history=messages_for_llm,
            )
        except Exception as exc:
            logger.error(str(exc))
            await self._ai_code_gen_repository.update_session_status(session_id, AICodeGenSessionStatus.FAILED)
            raise AICodeGenInvalidResponseError from exc

        await self._ai_code_gen_repository.add_message(
            AICodeGenMessageCreateDTO(
                session_id=session_id,
                role=AICodeGenRole.ASSISTANT,
                content=response.summary,
                meta={
                    'summary': response.summary,
                    'code': response.code,
                    'requirements': response.requirements,
                    'model': settings.OPENAI_MODEL,
                },
            )
        )
        await self._ai_code_gen_repository.update_session_status(
            session_id=session_id,
            status=AICodeGenSessionStatus.SUCCEEDED,
        )

    async def _build_llm_messages(self, session_id: int) -> list[LLMChatMessage]:
        history = await self._ai_code_gen_repository.get_messages(session_id)
        messages = [LLMChatMessage(role=LLMChatMemberRole.SYSTEM, content=SYSTEM_PROMPT)]
        for message in history:
            if message.role == LLMChatMemberRole.USER:
                messages.append(LLMChatMessage(role=LLMChatMemberRole.USER, content=message.content))
            elif message.role == LLMChatMemberRole.ASSISTANT:
                messages.append(LLMChatMessage(role=LLMChatMemberRole.ASSISTANT, content=message.content))
        return messages
