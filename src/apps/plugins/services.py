from uuid import UUID

from src.apps.plugins.dependencies.repositories_dependencies import PluginRepositoryDI
from src.apps.plugins.dto import PluginReadDTO
from src.apps.plugins.errors import (
    PluginNotFoundError,
    PluginAlreadyInProjectError,
    PluginIsNotInProjectError,
    PluginsLimitExceededError,
)
from src.apps.projects.dependencies.services_dependencies import ProjectServiceDI
from src.apps.users.dependencies.services_dependencies import UserServiceDI
from src.core.consts import MAX_PLUGINS_PER_PROJECT

PLUGINS_PER_PAGE = 9


class PluginService:
    def __init__(
        self,
        plugin_repository: PluginRepositoryDI,
        user_service: UserServiceDI,
        project_service: ProjectServiceDI,
    ):
        self._plugin_repository = plugin_repository
        self._user_service = user_service
        self._project_service = project_service

    async def get_plugins(self, page: int) -> list[PluginReadDTO]:
        return await self._plugin_repository.get_plugins(
            offset=(page - 1) * PLUGINS_PER_PAGE,
            limit=PLUGINS_PER_PAGE,
        )

    async def get_plugin(self, plugin_id: int) -> PluginReadDTO:
        plugin = await self._plugin_repository.get_plugin(plugin_id)
        if plugin is None:
            raise PluginNotFoundError
        return plugin

    async def add_plugin_to_project(self, user_id: UUID, project_id: int, plugin_id: int):
        project = await self._project_service.get_project_with_plugins(user_id=user_id, project_id=project_id)

        if project.contains_specific_plugin(plugin_id):
            raise PluginAlreadyInProjectError
        if len(project.plugins) >= MAX_PLUGINS_PER_PROJECT:
            raise PluginsLimitExceededError

        _ = await self.get_plugin(plugin_id)
        await self._plugin_repository.add_plugin_to_project(project_id=project_id, plugin_id=plugin_id)

    async def remove_plugin_from_project(self, user_id: UUID, project_id: int, plugin_id: int):
        project = await self._project_service.get_project_with_plugins(user_id=user_id, project_id=project_id)
        if not project.contains_specific_plugin(plugin_id):
            raise PluginIsNotInProjectError
        await self._plugin_repository.remove_plugin_from_project(project_id=project_id, plugin_id=plugin_id)
