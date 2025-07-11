from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core import settings


class Base(DeclarativeBase):
    pass


def get_postgres_dsn(
        user=settings.DB_USER,
        password=settings.DB_PASS,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
) -> str:
    return 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}'.format(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
    )


engine = create_async_engine(get_postgres_dsn())
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
