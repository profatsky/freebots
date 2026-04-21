from typing import Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from src.apps.ai_code_gen.enums import AICodeGenRole
from src.core.base_repository import BaseRepository
from src.apps.ai_code_gen.dto import (
    AICodeGenSessionCreateDTO,
    AICodeGenSessionReadDTO,
    AICodeGenMessageCreateDTO,
    AICodeGenMessageReadDTO,
    AICodeGenSessionWithMessagesReadDTO,
)
from src.apps.ai_code_gen.models import AICodeGenSessionModel, AICodeGenMessageModel


class AICodeGenRepository(BaseRepository):
    async def get_sessions(self, user_id: UUID, offset: int, limit: int) -> list[AICodeGenSessionReadDTO]:
        sessions = await self._session.execute(
            select(AICodeGenSessionModel)
            .where(AICodeGenSessionModel.user_id == user_id)
            .order_by(AICodeGenSessionModel.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return [session.to_dto() for session in sessions.scalars().all()]

    async def create_session(self, dto: AICodeGenSessionCreateDTO) -> AICodeGenSessionReadDTO:
        session = AICodeGenSessionModel.from_dto(dto)
        self._session.add(session)
        await self._session.commit()
        return session.to_dto()

    async def update_session_status(self, session_id: UUID, status) -> Optional[AICodeGenSessionReadDTO]:
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
        return message.to_dto()

    async def get_session(self, session_id: UUID) -> Optional[AICodeGenSessionReadDTO]:
        session = await self._get_session_model(session_id)
        if session is None:
            return None
        return session.to_dto()

    async def get_session_with_messages(self, session_id: UUID) -> Optional[AICodeGenSessionWithMessagesReadDTO]:
        session = await self._session.execute(
            select(AICodeGenSessionModel)
            .options(selectinload(AICodeGenSessionModel.messages))
            .where(AICodeGenSessionModel.session_id == session_id)
        )
        session = session.scalar()
        if session is None:
            return None
        return session.to_dto_with_messages()

    async def count_messages(self, session_id: UUID) -> int:
        result = await self._session.execute(
            select(func.count(AICodeGenMessageModel.message_id)).where(AICodeGenMessageModel.session_id == session_id)
        )
        return result.scalar_one()

    async def get_messages(self, session_id: UUID) -> list[AICodeGenMessageReadDTO]:
        result = await self._session.execute(
            select(AICodeGenMessageModel)
            .where(AICodeGenMessageModel.session_id == session_id)
            .order_by(AICodeGenMessageModel.created_at)
        )
        return [message.to_dto() for message in result.scalars().all()]

    async def get_latest_assistant_message(self, session_id: UUID) -> Optional[AICodeGenMessageReadDTO]:
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

    async def _get_session_model(self, session_id: UUID) -> Optional[AICodeGenSessionModel]:
        result = await self._session.execute(
            select(AICodeGenSessionModel).where(AICodeGenSessionModel.session_id == session_id)
        )
        return result.scalar()
