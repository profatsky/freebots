from typing import Optional

from sqlalchemy import select, delete, func
from sqlalchemy.orm import selectinload, joinedload

from src.blocks.models import BlockModel
from src.dialogues.models import DialogueModel
from src.infrastructure.db.dependencies import AsyncSessionDI
from src.projects.models import ProjectModel
from src.projects.schemas import (
    ProjectReadSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
    ProjectToGenerateCodeReadSchema,
)


class ProjectRepository:
    def __init__(self, session: AsyncSessionDI):
        self._session = session

    async def create_project(self, user_id: int, project_data: ProjectCreateSchema) -> ProjectReadSchema:
        project = ProjectModel(**project_data.model_dump(), user_id=user_id)
        self._session.add(project)
        await self._session.commit()
        return await self.get_project(project.project_id)

    async def get_projects(self, user_id: int) -> list[ProjectReadSchema]:
        projects = await self._session.execute(
            select(ProjectModel)
            .options(
                selectinload(ProjectModel.dialogues).joinedload(DialogueModel.trigger),
                selectinload(ProjectModel.plugins),
            )
            .where(ProjectModel.user_id == user_id)
        )
        projects = projects.unique().scalars().all()
        return [ProjectReadSchema.model_validate(project) for project in projects]

    async def get_project(self, project_id: int) -> Optional[ProjectReadSchema]:
        project = await self._get_project_model_instance(project_id)
        if not project:
            return
        return ProjectReadSchema.model_validate(project)

    async def get_project_to_generate_code(self, project_id: int) -> Optional[ProjectToGenerateCodeReadSchema]:
        project = await self._session.execute(
            select(ProjectModel)
            .options(
                selectinload(ProjectModel.plugins),
                selectinload(ProjectModel.dialogues).options(
                    joinedload(DialogueModel.trigger),
                    selectinload(DialogueModel.blocks).selectin_polymorphic(BlockModel.__subclasses__()),
                ),
            )
            .where(ProjectModel.project_id == project_id)
        )
        project = project.scalar()
        if project is None:
            return
        return ProjectToGenerateCodeReadSchema.model_validate(project)

    async def update_project(
        self,
        project_id: int,
        project_data: ProjectUpdateSchema,
    ) -> Optional[ProjectReadSchema]:
        project = await self._get_project_model_instance(project_id)
        if project is None:
            return

        project.name = project_data.name
        project.start_message = project_data.start_message
        project.start_keyboard_type = project_data.start_keyboard_type
        await self._session.commit()
        return ProjectReadSchema.model_validate(project)

    async def delete_project(self, project_id: int):
        await self._session.execute(
            delete(ProjectModel).where(
                ProjectModel.project_id == project_id,
            )
        )
        await self._session.commit()

    async def count_projects(self, user_id: int) -> int:
        return await self._session.scalar(
            select(func.count()).select_from(ProjectModel).where(ProjectModel.user_id == user_id)
        )

    async def _get_project_model_instance(self, project_id: int) -> Optional[ProjectModel]:
        project = await self._session.execute(
            select(ProjectModel)
            .options(
                selectinload(ProjectModel.dialogues).joinedload(DialogueModel.trigger),
                selectinload(ProjectModel.plugins),
            )
            .where(ProjectModel.project_id == project_id)
        )
        return project.scalar()
