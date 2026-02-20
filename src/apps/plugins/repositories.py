from typing import Optional

from sqlalchemy import select, insert, delete
from sqlalchemy.orm import selectinload

from src.apps.plugins.dto import PluginReadDTO
from src.apps.projects.models import ProjectModel
from src.core.base_repository import BaseRepository
from src.apps.plugins.models import PluginModel, projects_plugins


class PluginRepository(BaseRepository):
    async def get_plugins(self, offset: int, limit: int) -> list[PluginReadDTO]:
        plugins = await self._session.execute(
            select(PluginModel)
            .options(selectinload(PluginModel.triggers))
            .order_by(PluginModel.created_at)
            .offset(offset)
            .limit(limit)
        )
        return [plugin.to_dto() for plugin in plugins.scalars().all()]

    async def get_plugin(self, plugin_id: int) -> Optional[PluginReadDTO]:
        plugin = await self._session.execute(
            select(PluginModel).options(selectinload(PluginModel.triggers)).where(PluginModel.plugin_id == plugin_id)
        )
        plugin = plugin.scalar()
        if plugin is None:
            return None
        return plugin.to_dto()

    async def add_plugin_to_project(self, project_id: int, plugin_id: int):
        await self._session.execute(insert(projects_plugins).values(project_id=project_id, plugin_id=plugin_id))
        await self._session.commit()

    async def remove_plugin_from_project(self, project_id: int, plugin_id: int):
        await self._session.execute(
            delete(projects_plugins).where(
                projects_plugins.c.project_id == project_id,
                projects_plugins.c.plugin_id == plugin_id,
            )
        )
        await self._session.commit()

    async def get_plugins_from_project(self, project_id: int) -> list[PluginReadDTO]:
        project = await self._session.execute(
            select(ProjectModel)
            .options(
                selectinload(ProjectModel.plugins).selectinload(PluginModel.triggers),
            )
            .where(ProjectModel.project_id == project_id)
        )
        return [plugin.to_dto() for plugin in project.plugins.scalars().all()]
