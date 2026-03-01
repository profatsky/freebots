from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.api.v1.ai_code_gen.enums import AICodeGenRole
from src.apps.ai_code_gen.enums import AICodeGenSessionStatus


@dataclass(frozen=True)
class AICodeGenSessionCreateDTO:
    user_id: UUID
    status: AICodeGenSessionStatus


@dataclass(frozen=True)
class AICodeGenSessionReadDTO:
    session_id: int
    user_id: UUID
    status: AICodeGenSessionStatus
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class AICodeGenMessageCreateDTO:
    session_id: int
    role: AICodeGenRole
    content: str
    meta: Optional[dict]


@dataclass(frozen=True)
class AICodeGenMessageReadDTO:
    message_id: int
    session_id: int
    role: AICodeGenRole
    content: str
    meta: Optional[dict]
    created_at: datetime


@dataclass(frozen=True)
class AICodeGenSessionWithMessagesReadDTO(AICodeGenSessionReadDTO):
    messages: list[AICodeGenMessageReadDTO]
