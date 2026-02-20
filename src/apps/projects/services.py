from typing import Optional
from uuid import UUID

from src.apps.projects.dependencies.repositories_dependencies import ProjectRepositoryDI
from src.api.v1.projects.schemas import ProjectToGenerateCodeReadSchema
from src.apps.projects.dto import (
    ProjectCreateDTO,
    ProjectReadDTO,
    ProjectWithDialoguesAndPluginsReadDTO,
    ProjectUpdateDTO,
)
from src.apps.projects.errors import (
    ProjectNotFoundError,
    NoPermissionForProjectError,
    ProjectsLimitExceededError,
)
from src.apps.subscriptions.dependencies.services_dependencies import SubscriptionServiceDI
from src.core.config import MEDIA_DIR
from src.core.consts import MAX_PROJECTS_WITH_FREE_PLAN, MAX_PROJECTS_WITH_PRO_PLAN


class ProjectService:
    def __init__(
        self,
        project_repository: ProjectRepositoryDI,
        subscription_service: SubscriptionServiceDI,
    ):
        self._project_repository = project_repository
        self._subscription_service = subscription_service

    async def create_project(self, project: ProjectCreateDTO) -> ProjectReadDTO:
        project_count = await self._project_repository.count_projects(project.user_id)

        active_subscription = await self._subscription_service.get_active_subscription(project.user_id)
        max_projects = MAX_PROJECTS_WITH_PRO_PLAN if active_subscription else MAX_PROJECTS_WITH_FREE_PLAN
        if project_count >= max_projects:
            raise ProjectsLimitExceededError

        return await self._project_repository.create_project(project)

    async def get_projects_with_dialogues_and_plugins(
        self,
        user_id: UUID,
    ) -> list[ProjectWithDialoguesAndPluginsReadDTO]:
        return await self._project_repository.get_projects_with_dialogues_and_plugins(user_id)

    async def get_project_to_generate_code(
        self,
        user_id: UUID,
        project_id: int,
    ) -> Optional[ProjectToGenerateCodeReadSchema]:
        project = await self._project_repository.get_project_to_generate_code(project_id)
        if project is None:
            raise ProjectNotFoundError

        if project.user_id != user_id:
            raise NoPermissionForProjectError

        return project

    async def get_project(self, user_id: UUID, project_id: int) -> ProjectReadDTO:
        project = await self._project_repository.get_project(project_id)
        if project is None:
            raise ProjectNotFoundError

        if project.user_id != user_id:
            raise NoPermissionForProjectError

        return project

    async def update_project(self, project: ProjectUpdateDTO) -> Optional[ProjectReadDTO]:
        _ = await self.get_project(user_id=project.user_id, project_id=project.project_id)
        return await self._project_repository.update_project(project)

    async def delete_project(self, user_id: UUID, project_id: int):
        _ = await self.get_project(user_id=user_id, project_id=project_id)

        media_dir = MEDIA_DIR / 'users' / str(user_id) / 'projects' / str(project_id)
        if media_dir.exists():
            media_dir.rmdir()

        await self._project_repository.delete_project(project_id)

    async def count_projects(self, user_id: UUID) -> int:
        return await self._project_repository.count_projects(user_id)

    # async def raise_error_if_not_exists(self, user_id: UUID, project_id: int):
    #     if not await self._project_repository.exists_by_id(user_id, project_id):
    #         raise ProjectNotFoundError
