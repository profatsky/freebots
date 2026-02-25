from datetime import datetime
from typing import Optional, Self

from pydantic import BaseModel, Field

from src.apps.ai_code_gen.dto import AICodeGenSessionWithMessagesReadDTO
from src.apps.enums import AICodeGenRole, AICodeGenSessionStatus


class AICodeGenSessionCreateSchema(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)


class AICodeGenMessageCreateSchema(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)


class AICodeGenSessionReadSchema(BaseModel):
    session_id: int
    status: AICodeGenSessionStatus
    created_at: datetime
    updated_at: datetime

    model_config = {
        'from_attributes': True,
    }


class AICodeGenMessageReadSchema(BaseModel):
    message_id: int
    role: AICodeGenRole
    content: str
    meta: Optional[dict]
    created_at: datetime

    model_config = {
        'from_attributes': True,
    }


class AICodeGenSessionWithMessagesReadSchema(BaseModel):
    session: AICodeGenSessionReadSchema
    messages: list[AICodeGenMessageReadSchema]

    @classmethod
    def from_dto(cls, dto: AICodeGenSessionWithMessagesReadDTO) -> Self:
        return cls(
            session=AICodeGenSessionReadSchema.model_validate(dto.session),
            messages=[AICodeGenMessageReadSchema.model_validate(message) for message in dto.messages],
        )
