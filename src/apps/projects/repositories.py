from typing import Optional
from uuid import UUID

from sqlalchemy import select, delete, func, exists
from sqlalchemy.orm import selectinload, joinedload

from src.apps.blocks.models import BlockModel
from src.apps.plugins.models import PluginModel
from src.apps.projects.dto import (
    ProjectCreateDTO,
    ProjectReadDTO,
    ProjectWithDialoguesAndPluginsReadDTO,
    ProjectUpdateDTO,
)
from src.core.base_repository import BaseRepository
from src.apps.dialogues.models import DialogueModel
from src.apps.projects.models import ProjectModel
from src.api.v1.projects.schemas import ProjectToGenerateCodeReadSchema


class ProjectRepository(BaseRepository):
    async def create_project(self, project: ProjectCreateDTO) -> ProjectReadDTO:
        project = ProjectModel.from_dto(project)
        self._session.add(project)
        await self._session.commit()
        return project.to_dto()

    async def get_projects_with_dialogues_and_plugins(
        self,
        user_id: UUID,
    ) -> list[ProjectWithDialoguesAndPluginsReadDTO]:
        projects = await self._session.execute(
            select(ProjectModel)
            .options(
                selectinload(ProjectModel.dialogues).joinedload(DialogueModel.trigger),
                selectinload(ProjectModel.plugins).selectinload(PluginModel.triggers),
            )
            .where(ProjectModel.user_id == user_id)
        )
        projects = projects.unique().scalars().all()
        return [project.to_extended_dto() for project in projects]

    async def get_project(self, project_id: int) -> Optional[ProjectReadDTO]:
        project = await self._get_project_model_instance(project_id)
        if not project:
            return None
        return project.to_dto()

    async def get_project_to_generate_code(self, project_id: int) -> Optional[ProjectToGenerateCodeReadSchema]:
        project = await self._session.execute(
            select(ProjectModel)
            .options(
                selectinload(ProjectModel.plugins).selectinload(PluginModel.triggers),
                selectinload(ProjectModel.dialogues).options(
                    joinedload(DialogueModel.trigger),
                    selectinload(DialogueModel.blocks).selectin_polymorphic(BlockModel.__subclasses__()),
                ),
            )
            .where(ProjectModel.project_id == project_id)
        )
        project = project.scalar()
        if project is None:
            return None
        return ProjectToGenerateCodeReadSchema.model_validate(project)

    async def update_project(self, project: ProjectUpdateDTO) -> Optional[ProjectReadDTO]:
        project_for_update = await self._get_project_model_instance(project.project_id)
        if project_for_update is None:
            return None

        project_for_update.name = project.name
        project_for_update.start_message = project.start_message
        project_for_update.start_keyboard_type = project.start_keyboard_type
        await self._session.commit()
        return project_for_update.to_dto()

    async def delete_project(self, project_id: int):
        await self._session.execute(
            delete(ProjectModel).where(
                ProjectModel.project_id == project_id,
            )
        )
        await self._session.commit()

    async def count_projects(self, user_id: UUID) -> int:
        return await self._session.scalar(
            select(func.count()).select_from(ProjectModel).where(ProjectModel.user_id == user_id)
        )

    async def _get_project_model_instance(self, project_id: int) -> Optional[ProjectModel]:
        project = await self._session.execute(
            select(ProjectModel)
            .options(
                selectinload(ProjectModel.dialogues).joinedload(DialogueModel.trigger),
                selectinload(ProjectModel.plugins).selectinload(PluginModel.triggers),
            )
            .where(ProjectModel.project_id == project_id)
        )
        return project.scalar()

    async def exists_by_id(self, user_id: UUID, project_id: int) -> bool:
        return await self._session.scalar(
            select(
                exists().where(
                    ProjectModel.user_id == user_id,
                    ProjectModel.project_id == project_id,
                )
            )
        )
