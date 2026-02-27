import datetime
from typing import Self
from uuid import UUID

from sqlalchemy import DateTime, Enum, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.v1.ai_code_gen.enums import AICodeGenRole
from src.apps.ai_code_gen.enums import AICodeGenSessionStatus
from src.apps.ai_code_gen.dto import (
    AICodeGenSessionCreateDTO,
    AICodeGenSessionReadDTO,
    AICodeGenMessageCreateDTO,
    AICodeGenMessageReadDTO,
    AICodeGenSessionWithMessagesReadDTO,
    AICodeGenMessageMetaDTO,
)
from src.infrastructure.db.sessions import Base


class AICodeGenSessionModel(Base):
    __tablename__ = 'ai_codegen_sessions'

    session_id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[AICodeGenSessionStatus] = mapped_column(
        Enum(AICodeGenSessionStatus).values_callable,
        nullable=False,
        default=AICodeGenSessionStatus.QUEUED,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))
    user: Mapped['UserModel'] = relationship(back_populates='ai_codegen_sessions')

    messages: Mapped[list['AICodeGenMessageModel']] = relationship(
        back_populates='session',
        cascade='all, delete-orphan',
        order_by='AICodeGenMessageModel.created_at',
    )

    @classmethod
    def from_dto(cls, dto: AICodeGenSessionCreateDTO) -> Self:
        return cls(
            user_id=dto.user_id,
            status=dto.status,
        )

    def to_dto(self) -> AICodeGenSessionReadDTO:
        return AICodeGenSessionReadDTO(
            session_id=self.session_id,
            user_id=self.user_id,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def to_dto_with_messages(self) -> AICodeGenSessionWithMessagesReadDTO:
        messages = [message.to_dto() for message in self.messages]
        return AICodeGenSessionWithMessagesReadDTO(
            session_id=self.session_id,
            user_id=self.user_id,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at,
            messages=messages,
        )


class AICodeGenMessageModel(Base):
    __tablename__ = 'ai_codegen_messages'

    message_id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[AICodeGenRole] = mapped_column(Enum(AICodeGenRole).values_callable, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    meta: Mapped[dict] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    session_id: Mapped[int] = mapped_column(ForeignKey('ai_codegen_sessions.session_id', ondelete='CASCADE'))
    session: Mapped['AICodeGenSessionModel'] = relationship(back_populates='messages')

    @classmethod
    def from_dto(cls, dto: AICodeGenMessageCreateDTO) -> Self:
        return cls(
            session_id=dto.session_id,
            role=dto.role,
            content=dto.content,
            meta=dto.meta.__dict__ if dto.meta else None,
        )

    def to_dto(self) -> AICodeGenMessageReadDTO:
        meta = None
        if self.meta:
            meta = AICodeGenMessageMetaDTO(
                summary=self.meta['summary'],
                main_py=self.meta['main_py'],
                requirements=self.meta['requirements'],
                dockerfile=self.meta['dockerfile'],
                model=self.meta['model'],
                # usage=None,
            )
        return AICodeGenMessageReadDTO(
            message_id=self.message_id,
            session_id=self.session_id,
            role=self.role,
            content=self.content,
            meta=meta,
            created_at=self.created_at,
        )
