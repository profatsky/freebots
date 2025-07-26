import os
import shutil
from typing import Optional

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


class ProjectService:
    def __init__(self, project_repository: ProjectRepositoryDI):
        self._project_repository = project_repository

    async def create_project(self, user_id: int, project_data: ProjectCreateSchema) -> ProjectReadSchema:
        project_count = await self._project_repository.count_projects(user_id)
        if project_count >= 5:
            raise ProjectsLimitExceededError

        return await self._project_repository.create_project(
            user_id=user_id,
            project_data=project_data,
        )

    async def get_projects(self, user_id: int) -> list[ProjectReadSchema]:
        return await self._project_repository.get_projects(user_id)

    async def get_project_to_generate_code(
        self,
        user_id: int,
        project_id: int,
    ) -> Optional[ProjectToGenerateCodeReadSchema]:
        project = await self._project_repository.get_project_to_generate_code(project_id)
        if project is None:
            raise ProjectNotFoundError

        if project.user_id != user_id:
            raise NoPermissionForProjectError

        return project

    async def get_project(self, user_id: int, project_id: int) -> ProjectReadSchema:
        project = await self._project_repository.get_project(project_id)
        if project is None:
            raise ProjectNotFoundError

        if project.user_id != user_id:
            raise NoPermissionForProjectError

        return project

    async def update_project(
        self,
        user_id: int,
        project_id: int,
        project_data: ProjectUpdateSchema,
    ) -> Optional[ProjectReadSchema]:
        _ = await self.get_project(
            user_id=user_id,
            project_id=project_id,
        )
        return await self._project_repository.update_project(
            project_id=project_id,
            project_data=project_data,
        )

    async def delete_project(self, user_id: int, project_id: int):
        _ = await self.get_project(
            user_id=user_id,
            project_id=project_id,
        )

        media_dir_path = os.path.join('src', 'media', 'users', str(user_id), 'projects', str(project_id))
        if os.path.exists(media_dir_path):
            shutil.rmtree(media_dir_path)

        await self._project_repository.delete_project(project_id)
