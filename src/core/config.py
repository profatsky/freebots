from datetime import timedelta
from pathlib import Path
from typing import Annotated

from authx import AuthXConfig
from fastapi.security import OAuth2PasswordBearer
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict, NoDecode
from yookassa import Configuration


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='allow')

    DEBUG: bool = False

    CLIENT_APP_URL: str

    JWT_SECRET: str

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_USER: str
    REDIS_USER_PASSWORD: str

    AUTH_BOT_SECRET: str

    YOOKASSA_SHOP_ID: str
    YOOKASSA_API_KEY: str
    YOOKASSA_IPS: Annotated[list[str], NoDecode]

    TEST_DB_NAME: str

    OPENAI_API_KEY: str
    OPENAI_MODEL: str = 'gpt-4o-mini'
    OPENAI_TEMPERATURE: float = 0.2
    OPENAI_MAX_OUTPUT_TOKENS: int = 12000

    AI_CODEGEN_MAX_PROMPT_CHARS: int = 4000
    AI_CODEGEN_MAX_MAIN_PY_CHARS: int = 60000
    AI_CODEGEN_MAX_REQUIREMENTS_CHARS: int = 2000
    AI_CODEGEN_MAX_DOCKERFILE_CHARS: int = 4000
    AI_CODEGEN_MAX_MESSAGES_PER_SESSION: int = 20

    @field_validator('YOOKASSA_IPS', mode='before')
    @classmethod
    def validate_yookassa_ips(cls, value: str) -> list[str]:
        return value.split(',')


settings = Settings()

# Auth
auth_config = AuthXConfig(
    JWT_ALGORITHM='HS256',
    JWT_SECRET_KEY=settings.JWT_SECRET,
    JWT_TOKEN_LOCATION=['headers'],
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=30),
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/swagger_login')

# Payments
Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_API_KEY

# Media
MEDIA_DIR = Path('src') / 'media'

# Code templates
BOT_TEMPLATES_DIR = Path('src') / 'apps' / 'code_gen' / 'bot_templates' / 'project_structure'
