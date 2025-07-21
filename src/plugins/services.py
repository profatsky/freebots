from src.plugins.dependencies.repositories_dependencies import PluginRepositoryDI
from src.plugins.exceptions.services_exceptions import (
    PluginNotFoundError,
    PluginAlreadyInProjectError,
    PluginIsNotInProjectError,
)
from src.plugins.schemas import PluginReadSchema
from src.projects.dependencies.services_dependencies import ProjectServiceDI
from src.projects.schemas import ProjectReadSchema
from src.users.dependencies.services_dependencies import UserServiceDI

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

    async def get_plugins(self, page: int) -> list[PluginReadSchema]:
        return await self._plugin_repository.get_plugins(
            offset=(page - 1) * PLUGINS_PER_PAGE,
            limit=PLUGINS_PER_PAGE,
        )

    async def get_plugin(self, plugin_id: int) -> PluginReadSchema:
        plugin = await self._plugin_repository.get_plugin(plugin_id)
        if plugin is None:
            raise PluginNotFoundError
        return plugin

    async def add_plugin_to_project(self, user_id: int, project_id: int, plugin_id: int) -> PluginReadSchema:
        project = await self._project_service.get_project(
            user_id=user_id,
            project_id=project_id,
        )

        if self._project_contain_plugin_with_specified_id(project, plugin_id):
            raise PluginAlreadyInProjectError

        _ = await self.get_plugin(plugin_id)

        # TODO add a limit on the number of plugins in a project
        return await self._plugin_repository.add_plugin_to_project(
            project_id=project_id,
            plugin_id=plugin_id,
        )

    async def remove_plugin_from_project(self, user_id: int, project_id: int, plugin_id: int):
        project = await self._project_service.get_project(
            user_id=user_id,
            project_id=project_id,
        )

        if not self._project_contain_plugin_with_specified_id(project, plugin_id):
            raise PluginIsNotInProjectError

        await self._plugin_repository.remove_plugin_from_project(
            project_id=project_id,
            plugin_id=plugin_id,
        )

    def _project_contain_plugin_with_specified_id(self, project: ProjectReadSchema, plugin_id: int) -> bool:
        project_plugins_ids = [plugin.plugin_id for plugin in project.plugins]
        return plugin_id in project_plugins_ids
