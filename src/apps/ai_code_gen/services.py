import io
import zipfile
from uuid import UUID

from loguru import logger

from src.api.v1.ai_code_gen.enums import AICodeGenRole
from src.apps.ai_code_gen.dependencies.repositories_dependencies import AICodeGenRepositoryDI
from src.apps.ai_code_gen.dto import (
    AICodeGenSessionCreateDTO,
    AICodeGenMessageCreateDTO,
    AICodeGenSessionWithMessagesReadDTO,
    AICodeGenMessageMetaDTO,
)
from src.apps.ai_code_gen.llm_schemas import AICodeGenLLMResponse
from src.apps.ai_code_gen.errors import (
    AICodeGenSessionNotFoundError,
    AICodeGenSessionNoPermissionError,
    AICodeGenPromptTooLongError,
    AICodeGenMessagesLimitExceededError,
    AICodeGenInvalidResponseError,
    AICodeGenResponseTooLongError,
    AICodeGenNoAssistantMessageError,
)
from src.apps.ai_code_gen.enums import AICodeGenSessionStatus
from src.core.config import settings
from src.infrastructure.llm.cli.openai import AsyncOpenAICli
from src.infrastructure.llm.enums import LLMChatMemberRole
from src.infrastructure.llm.types import LLMChatMessage

SYSTEM_PROMPT = (
    'Ты создаешь Telegram-бота на Python с использованием aiogram 3. '
    'Верни ответ строго в JSON формате с ключами: summary, main_py, requirements, dockerfile. '
    'Не используй markdown и не оборачивай JSON в кодовые блоки. '
    'main_py должен содержать полный код бота в одном файле. '
    'requirements должен содержать минимальные зависимости. '
    'dockerfile должен быть минимальным и запускать main.py. '
    'Не включай секреты и токены. Используй переменную окружения BOT_TOKEN.'
)


class AICodeGenService:
    def __init__(
        self,
        ai_code_gen_repository: AICodeGenRepositoryDI,
    ):
        self._ai_code_gen_repository = ai_code_gen_repository
        self._client = AsyncOpenAICli(model=settings.OPENAI_MODEL)

    async def create_session(self, user_id: UUID, prompt: str) -> AICodeGenSessionWithMessagesReadDTO:
        self._validate_prompt(prompt)
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
        self._validate_prompt(prompt)
        await self._assert_session_owner(user_id=user_id, session_id=session_id)

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
        if session is None:
            raise AICodeGenSessionNotFoundError
        if session.user_id != user_id:
            raise AICodeGenSessionNoPermissionError
        return session

    async def get_zip(self, user_id: UUID, session_id: int) -> io.BytesIO:
        await self._assert_session_owner(user_id=user_id, session_id=session_id)
        last_message = await self._ai_code_gen_repository.get_latest_assistant_message(session_id)
        if last_message is None or not last_message.meta:
            raise AICodeGenNoAssistantMessageError

        main_py = last_message.meta.main_py
        requirements = last_message.meta.requirements
        dockerfile = last_message.meta.dockerfile
        if not main_py or not requirements or not dockerfile:
            raise AICodeGenNoAssistantMessageError

        zip_data = io.BytesIO()
        with zipfile.ZipFile(zip_data, mode='w') as zipf:
            zipf.writestr('main.py', main_py)
            zipf.writestr('requirements.txt', requirements)
            zipf.writestr('Dockerfile', dockerfile)
        zip_data.seek(0)
        return zip_data

    async def _generate_and_store_response(self, session_id: int) -> None:
        await self._ai_code_gen_repository.update_session_status(session_id, AICodeGenSessionStatus.RUNNING)
        messages_for_llm = await self._build_llm_messages(session_id)

        try:
            response = await self._client.make_structured_request(
                object_type=AICodeGenLLMResponse,
                history=messages_for_llm,
            )
        except Exception as exc:
            logger.error(str(exc))
            await self._ai_code_gen_repository.update_session_status(session_id, AICodeGenSessionStatus.FAILED)
            raise AICodeGenInvalidResponseError from exc

        summary = response.summary
        main_py = response.main_py
        requirements = '\n'.join(response.requirements)
        dockerfile = response.dockerfile

        try:
            self._validate_response(main_py=main_py, requirements=requirements, dockerfile=dockerfile)
        except (AICodeGenResponseTooLongError, AICodeGenInvalidResponseError):
            await self._ai_code_gen_repository.update_session_status(session_id, AICodeGenSessionStatus.FAILED)
            raise

        await self._ai_code_gen_repository.add_message(
            AICodeGenMessageCreateDTO(
                session_id=session_id,
                role=AICodeGenRole.ASSISTANT,
                content=main_py,
                meta=AICodeGenMessageMetaDTO(
                    summary=summary,
                    main_py=main_py,
                    requirements=requirements,
                    dockerfile=dockerfile,
                    model=settings.OPENAI_MODEL,
                    usage=None,
                ),
            )
        )

        await self._ai_code_gen_repository.update_session_status(session_id, AICodeGenSessionStatus.SUCCEEDED)

    async def _build_llm_messages(self, session_id: int) -> list[LLMChatMessage]:
        history = await self._ai_code_gen_repository.get_messages(session_id)
        messages = [LLMChatMessage(role=LLMChatMemberRole.SYSTEM, content=SYSTEM_PROMPT)]
        for message in history:
            if message.role == LLMChatMemberRole.USER:
                messages.append(LLMChatMessage(role=LLMChatMemberRole.USER, content=message.content))
            elif message.role == LLMChatMemberRole.ASSISTANT:
                summary = ''
                if message.meta and isinstance(message.meta, dict):
                    summary = message.meta.get('summary') or ''
                content = summary or 'Предыдущий ответ уже был сгенерирован.'
                messages.append(LLMChatMessage(role=LLMChatMemberRole.ASSISTANT, content=content))
        return messages

    def _validate_prompt(self, prompt: str) -> None:
        if len(prompt) > settings.AI_CODEGEN_MAX_PROMPT_CHARS:
            raise AICodeGenPromptTooLongError

    def _validate_response(self, main_py: str, requirements: str, dockerfile: str) -> None:
        if (
            len(main_py) > settings.AI_CODEGEN_MAX_MAIN_PY_CHARS
            or len(requirements) > settings.AI_CODEGEN_MAX_REQUIREMENTS_CHARS
            or len(dockerfile) > settings.AI_CODEGEN_MAX_DOCKERFILE_CHARS
        ):
            raise AICodeGenResponseTooLongError
        if not main_py or not requirements or not dockerfile:
            raise AICodeGenInvalidResponseError

    async def _assert_session_owner(self, user_id: UUID, session_id: int) -> None:
        session = await self._ai_code_gen_repository.get_session(session_id)
        if session is None:
            raise AICodeGenSessionNotFoundError
        if session.user_id != user_id:
            raise AICodeGenSessionNoPermissionError
