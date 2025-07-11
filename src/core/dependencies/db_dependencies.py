from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_async_session

AsyncSessionDI = Annotated[AsyncSession, Depends(get_async_session)]
