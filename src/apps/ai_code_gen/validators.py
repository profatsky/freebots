from src.apps.ai_code_gen.errors import AICodeGenPromptTooLongError
from src.core.config import settings


def validate_user_prompt(prompt: str):
    if len(prompt) > settings.AI_CODEGEN_MAX_PROMPT_CHARS:
        raise AICodeGenPromptTooLongError
