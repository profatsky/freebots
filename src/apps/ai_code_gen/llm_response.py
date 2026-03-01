from pydantic import BaseModel, Field, field_validator

from src.core.config import settings


class LLMResponse(BaseModel):
    summary: str
    # TODO: rename to code file or something else
    main_py: str = Field(max_length=settings.AI_CODEGEN_MAX_MAIN_PY_CHARS)
    requirements: list[str]
    # TODO: generate manually without LLM
    dockerfile: str = Field(max_length=settings.AI_CODEGEN_MAX_DOCKERFILE_CHARS)

    @field_validator('requirements', mode='after')
    @classmethod
    def validate_requirements(cls, value: list[str]) -> list[str]:
        if len('\n'.join(value)) > settings.AI_CODEGEN_MAX_REQUIREMENTS_CHARS:
            raise ValueError('Invalid requirements')
        return value
