from sqlalchemy import func, select

from src.infrastructure.db.dependencies import AsyncSessionDI
from src.projects.models import ProjectModel
from src.users.models import UserModel


class StatisticRepository:
    def __init__(self, session: AsyncSessionDI):
        self._session = session

    async def count_users(self) -> int:
        return await self._session.scalar(select(func.count()).select_from(UserModel))

    async def count_projects(self) -> int:
        return await self._session.scalar(select(func.count()).select_from(ProjectModel))
