from pydantic import BaseModel, Field, field_validator

from src.core.config import settings


class LLMResponse(BaseModel):
    summary: str
    code: str = Field(max_length=settings.AI_CODEGEN_MAX_CODE_CHARS)
    requirements: list[str]

    @field_validator('requirements', mode='after')
    @classmethod
    def validate_requirements(cls, value: list[str]) -> list[str]:
        if len('\n'.join(value)) > settings.AI_CODEGEN_MAX_REQUIREMENTS_CHARS:
            raise ValueError('Invalid requirements')
        return value
