from uuid import UUID

from src.apps.statistics.dependencies.repositories_dependencies import StatisticRepositoryDI
from src.apps.statistics.schemas import StatisticSchema
from src.apps.users.errors import DontHavePermissionError
from src.apps.users.dependencies.services_dependencies import UserServiceDI


class StatisticService:
    def __init__(
        self,
        user_service: UserServiceDI,
        statistic_repository: StatisticRepositoryDI,
    ):
        self._user_service = user_service
        self._statistic_repository = statistic_repository

    async def get_statistic(self, user_id: UUID) -> StatisticSchema:
        user = await self._user_service.get_user_by_id(user_id)
        if user is None or not user.is_superuser:
            raise DontHavePermissionError

        user_count = await self._statistic_repository.count_users()
        project_count = await self._statistic_repository.count_projects()

        return StatisticSchema(
            user_count=user_count,
            project_count=project_count,
        )

    async def save_download_to_history(self, user_id: UUID, project_id: int) -> None:
        await self._statistic_repository.save_download_to_history(user_id, project_id)
