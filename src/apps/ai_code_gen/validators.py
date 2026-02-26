from typing import Optional
from uuid import UUID

from src.apps.ai_code_gen.dto import AICodeGenSessionReadDTO
from src.apps.ai_code_gen.errors import (
    AICodeGenPromptTooLongError,
    AICodeGenSessionNotFoundError,
    AICodeGenSessionNoPermissionError,
)
from src.core.config import settings


def validate_user_prompt(prompt: str):
    if len(prompt) > settings.AI_CODEGEN_MAX_PROMPT_CHARS:
        raise AICodeGenPromptTooLongError


def validate_session_and_ownership(session: Optional[AICodeGenSessionReadDTO], user_id: UUID):
    if session is None:
        raise AICodeGenSessionNotFoundError
    if session.user_id != user_id:
        raise AICodeGenSessionNoPermissionError
