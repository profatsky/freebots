from typing import Annotated

from fastapi import Depends, Request

from src.infrastructure.cache.client import CacheClient


def get_cache_client(request: Request) -> CacheClient:
    return request.state.cache_cli


CacheClientDI = Annotated[CacheClient, Depends(get_cache_client)]
