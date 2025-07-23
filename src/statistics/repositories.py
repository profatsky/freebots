from sqlalchemy import func, select

from src.core.base_repository import BaseRepository
from src.projects.models import ProjectModel
from src.users.models import UserModel


class StatisticRepository(BaseRepository):
    async def count_users(self) -> int:
        return await self._session.scalar(select(func.count()).select_from(UserModel))

    async def count_projects(self) -> int:
        return await self._session.scalar(select(func.count()).select_from(ProjectModel))
