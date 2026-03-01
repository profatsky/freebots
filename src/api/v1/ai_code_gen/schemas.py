from datetime import datetime
from typing import Optional, Self

from pydantic import BaseModel, Field

from src.api.v1.ai_code_gen.enums import AICodeGenRole
from src.apps.ai_code_gen.dto import (
    AICodeGenSessionWithMessagesReadDTO,
    AICodeGenMessageReadDTO,
    AICodeGenSessionReadDTO,
)
from src.apps.ai_code_gen.enums import AICodeGenSessionStatus
from src.core.config import settings


class AICodeGenSessionCreateSchema(BaseModel):
    prompt: str = Field(min_length=1, max_length=settings.AI_CODEGEN_MAX_PROMPT_CHARS)


class AICodeGenSessionReadSchema(BaseModel):
    session_id: int
    status: AICodeGenSessionStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dto(cls, session: AICodeGenSessionReadDTO) -> Self:
        return cls(
            session_id=session.session_id,
            status=session.status,
            created_at=session.created_at,
            updated_at=session.updated_at,
        )


class AICodeGenMessageCreateSchema(BaseModel):
    prompt: str = Field(min_length=1, max_length=settings.AI_CODEGEN_MAX_PROMPT_CHARS)


class AICodeGenMessageReadSchema(BaseModel):
    message_id: int
    role: AICodeGenRole
    content: str
    meta: Optional[dict]
    created_at: datetime

    @classmethod
    def from_dto(cls, dto: AICodeGenMessageReadDTO) -> Self:
        return cls(
            message_id=dto.message_id,
            role=dto.role,
            content=dto.content,
            meta=dto.meta,
            created_at=dto.created_at,
        )


class AICodeGenSessionWithMessagesReadSchema(BaseModel):
    session: AICodeGenSessionReadSchema
    messages: list[AICodeGenMessageReadSchema]

    @classmethod
    def from_dto(cls, dto: AICodeGenSessionWithMessagesReadDTO) -> Self:
        session = AICodeGenSessionReadSchema(
            session_id=dto.session_id,
            status=dto.status,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
        messages = [AICodeGenMessageReadSchema.from_dto(message) for message in dto.messages]
        return cls(
            session=session,
            messages=messages,
        )
