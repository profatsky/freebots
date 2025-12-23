from typing import Self, Any

from redis.asyncio import Redis

from src.core.config import settings


class CacheClient:
    def __init__(self):
        self._client = None

    async def __aenter__(self) -> Self:
        self._client = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            username=settings.REDIS_USER,
            password=settings.REDIS_USER_PASSWORD,
        )
        await self._client.ping()
        return self

    async def get(self, name: str) -> Any:
        return await self._client.get(name)

    async def set(self, name: str, value: int | float | str, ex: int) -> None:
        await self._client.set(name=name, value=value, ex=ex)

    async def delete(self, name: str) -> None:
        await self._client.delete(name)

    async def incr(self, name: str, amount: int = 1) -> Any:
        return await self._client.incr(name, amount)

    async def ttl(self, name: str) -> Any:
        return await self._client.ttl(name)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
