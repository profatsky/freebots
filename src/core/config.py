from datetime import timedelta

from authx import AuthXConfig
from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='allow')

    CLIENT_APP_URL: str

    JWT_SECRET: str

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    TEST_DB_NAME: str


settings = Settings()
auth_config = AuthXConfig(
    JWT_ALGORITHM='HS256',
    JWT_SECRET_KEY=settings.JWT_SECRET,
    JWT_TOKEN_LOCATION=['headers'],
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=30),
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/swagger_login')
