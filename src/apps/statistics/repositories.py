from uuid import UUID

from sqlalchemy import func, select

from src.apps.statistics.models import DownloadModel
from src.core.base_repository import BaseRepository
from src.apps.projects.models import ProjectModel
from src.apps.users.models import UserModel


class StatisticRepository(BaseRepository):
    async def count_users(self) -> int:
        return await self._session.scalar(select(func.count()).select_from(UserModel))

    async def count_projects(self) -> int:
        return await self._session.scalar(select(func.count()).select_from(ProjectModel))

    async def save_download_to_history(self, user_id: UUID, project_id: int) -> None:
        download = DownloadModel(user_id=user_id, project_id=project_id)
        self._session.add(download)
        await self._session.commit()
