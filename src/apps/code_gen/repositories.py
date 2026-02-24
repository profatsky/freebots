from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.apps.blocks.models import BlockModel
from src.apps.code_gen.dto import ProjectCodeGenReadDTO
from src.apps.dialogues.models import DialogueModel
from src.apps.plugins.models import PluginModel
from src.apps.projects.models import ProjectModel
from src.core.base_repository import BaseRepository


class CodeGenRepository(BaseRepository):
    async def get_project_to_generate_code(self, project_id: int) -> Optional[ProjectCodeGenReadDTO]:
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
        return project.to_code_gen_dto()
