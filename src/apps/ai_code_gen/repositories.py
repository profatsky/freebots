from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from src.core.base_repository import BaseRepository
from src.apps.ai_code_gen.dto import (
    AICodeGenSessionCreateDTO,
    AICodeGenSessionReadDTO,
    AICodeGenMessageCreateDTO,
    AICodeGenMessageReadDTO,
)
from src.apps.ai_code_gen.models import AICodeGenSessionModel, AICodeGenMessageModel
from src.apps.enums import AICodeGenRole


class AICodeGenRepository(BaseRepository):
    async def create_session(self, dto: AICodeGenSessionCreateDTO) -> AICodeGenSessionReadDTO:
        session = AICodeGenSessionModel.from_dto(dto)
        self._session.add(session)
        await self._session.commit()
        await self._session.refresh(session)
        return session.to_dto()

    async def update_session_status(self, session_id: int, status) -> Optional[AICodeGenSessionReadDTO]:
        session = await self._get_session_model(session_id)
        if session is None:
            return None
        session.status = status
        await self._session.commit()
        await self._session.refresh(session)
        return session.to_dto()

    async def add_message(self, dto: AICodeGenMessageCreateDTO) -> AICodeGenMessageReadDTO:
        message = AICodeGenMessageModel.from_dto(dto)
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message.to_dto()

    async def get_session(self, session_id: int) -> Optional[AICodeGenSessionReadDTO]:
        session = await self._get_session_model(session_id)
        if session is None:
            return None
        return session.to_dto()

    async def get_session_with_messages(self, session_id: int) -> Optional[AICodeGenSessionModel]:
        result = await self._session.execute(
            select(AICodeGenSessionModel)
            .options(selectinload(AICodeGenSessionModel.messages))
            .where(AICodeGenSessionModel.session_id == session_id)
        )
        return result.scalar()

    async def count_messages(self, session_id: int) -> int:
        result = await self._session.execute(
            select(func.count(AICodeGenMessageModel.message_id)).where(AICodeGenMessageModel.session_id == session_id)
        )
        return result.scalar_one()

    async def get_messages_for_context(self, session_id: int, limit: int) -> list[AICodeGenMessageReadDTO]:
        result = await self._session.execute(
            select(AICodeGenMessageModel)
            .where(AICodeGenMessageModel.session_id == session_id)
            .order_by(AICodeGenMessageModel.created_at.asc())
        )
        messages = result.scalars().all()
        if limit > 0:
            messages = messages[-limit:]
        return [message.to_dto() for message in messages]

    async def get_latest_assistant_message(self, session_id: int) -> Optional[AICodeGenMessageReadDTO]:
        result = await self._session.execute(
            select(AICodeGenMessageModel)
            .where(AICodeGenMessageModel.session_id == session_id)
            .where(AICodeGenMessageModel.role == AICodeGenRole.ASSISTANT)
            .order_by(AICodeGenMessageModel.created_at.desc())
        )
        message = result.scalars().first()
        if message is None:
            return None
        return message.to_dto()

    async def _get_session_model(self, session_id: int) -> Optional[AICodeGenSessionModel]:
        result = await self._session.execute(
            select(AICodeGenSessionModel).where(AICodeGenSessionModel.session_id == session_id)
        )
        return result.scalar()
