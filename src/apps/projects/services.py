import os
import shutil
from typing import Optional
from uuid import UUID

from src.apps.projects.dependencies.repositories_dependencies import ProjectRepositoryDI
from src.apps.projects.schemas import (
    ProjectReadSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
    ProjectToGenerateCodeReadSchema,
)
from src.apps.projects.exceptions.services_exceptions import (
    ProjectNotFoundError,
    NoPermissionForProjectError,
    ProjectsLimitExceededError,
)
from src.apps.subscriptions.dependencies.services_dependencies import SubscriptionServiceDI
from src.core.consts import MAX_PROJECTS_WITH_FREE_PLAN, MAX_PROJECTS_WITH_PRO_PLAN


class ProjectService:
    def __init__(
        self,
        project_repository: ProjectRepositoryDI,
        subscription_service: SubscriptionServiceDI,
    ):
        self._project_repository = project_repository
        self._subscription_service = subscription_service

    async def create_project(self, user_id: UUID, project_data: ProjectCreateSchema) -> ProjectReadSchema:
        project_count = await self._project_repository.count_projects(user_id)

        active_subscription = await self._subscription_service.get_active_subscription(user_id)
        max_projects = MAX_PROJECTS_WITH_PRO_PLAN if active_subscription else MAX_PROJECTS_WITH_FREE_PLAN

        if project_count >= max_projects:
            raise ProjectsLimitExceededError

        return await self._project_repository.create_project(
            user_id=user_id,
            project_data=project_data,
        )

    async def get_projects(self, user_id: UUID) -> list[ProjectReadSchema]:
        return await self._project_repository.get_projects(user_id)

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

    async def get_project(self, user_id: UUID, project_id: int) -> ProjectReadSchema:
        project = await self._project_repository.get_project(project_id)
        if project is None:
            raise ProjectNotFoundError

        if project.user_id != user_id:
            raise NoPermissionForProjectError

        return project

    async def update_project(
        self,
        user_id: UUID,
        project_id: int,
        project_data: ProjectUpdateSchema,
    ) -> Optional[ProjectReadSchema]:
        await self.raise_error_if_not_exists(user_id, project_id)
        return await self._project_repository.update_project(
            project_id=project_id,
            project_data=project_data,
        )

    async def delete_project(self, user_id: UUID, project_id: int):
        await self.raise_error_if_not_exists(user_id, project_id)

        media_dir_path = os.path.join('src', 'media', 'users', str(user_id), 'projects', str(project_id))
        if os.path.exists(media_dir_path):
            shutil.rmtree(media_dir_path)

        await self._project_repository.delete_project(project_id)

    async def count_projects(self, user_id: UUID) -> int:
        return await self._project_repository.count_projects(user_id)

    async def raise_error_if_not_exists(self, user_id: UUID, project_id: int):
        if not await self._project_repository.exists_by_id(user_id, project_id):
            raise ProjectNotFoundError
