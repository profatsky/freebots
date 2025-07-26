from typing import Optional

from sqlalchemy import select, insert, delete

from src.core.base_repository import BaseRepository
from src.apps.plugins.models import PluginModel, projects_plugins
from src.apps.plugins.schemas import PluginReadSchema


class PluginRepository(BaseRepository):
    async def get_plugins(self, offset: int, limit: int) -> list[PluginReadSchema]:
        plugins = await self._session.execute(
            select(PluginModel).order_by(PluginModel.created_at).offset(offset).limit(limit)
        )
        return [PluginReadSchema.model_validate(plugin) for plugin in plugins.scalars().all()]

    async def get_plugin(self, plugin_id: int) -> Optional[PluginReadSchema]:
        plugin = await self._session.execute(select(PluginModel).where(PluginModel.plugin_id == plugin_id))
        plugin = plugin.scalar()
        if plugin is None:
            return
        return PluginReadSchema.model_validate(plugin)

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
