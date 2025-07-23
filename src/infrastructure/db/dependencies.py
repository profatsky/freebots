from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.sessions import get_async_session

AsyncSessionDI = Annotated[AsyncSession, Depends(get_async_session)]
