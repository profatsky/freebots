from typing import Annotated

from fastapi import APIRouter, Query, status, Body, Depends

from src.apps.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.apps.plugins.dependencies.services_dependencies import PluginServiceDI
from src.apps.plugins.exceptions.http_exceptions import (
    PluginNotFoundHTTPException,
    PluginAlreadyInProjectHTTPException,
    PluginIsNotInProjectHTTPException,
    PluginsLimitExceededHTTPException,
)
from src.apps.plugins.exceptions.services_exceptions import (
    PluginNotFoundError,
    PluginAlreadyInProjectError,
    PluginIsNotInProjectError,
    PluginsLimitExceededError,
)
from src.apps.plugins.schemas import PluginReadSchema
from src.api.v1.projects.exceptions import (
    ProjectNotFoundHTTPException,
    NoPermissionForProjectHTTPException,
)
from src.apps.projects.errors import ProjectNotFoundError, NoPermissionForProjectError

router = APIRouter(
    tags=['Plugins'],
    dependencies=[Depends(access_token_required)],
)


@router.get(
    '/plugins',
    response_model=list[PluginReadSchema],
)
async def get_plugins(
    plugin_service: PluginServiceDI,
    page: Annotated[int, Query(ge=1)] = 1,
):
    return await plugin_service.get_plugins(page)


@router.get(
    '/plugins/{plugin_id}',
    response_model=PluginReadSchema,
)
async def get_plugin(
    plugin_id: int,
    plugin_service: PluginServiceDI,
):
    try:
        return await plugin_service.get_plugin(plugin_id)
    except PluginNotFoundError:
        raise PluginNotFoundHTTPException


@router.post(
    '/projects/{project_id}/plugins',
    status_code=status.HTTP_201_CREATED,
)
async def add_plugin_to_project(
    project_id: int,
    plugin_id: Annotated[int, Body(embed=True)],
    plugin_service: PluginServiceDI,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        await plugin_service.add_plugin_to_project(
            user_id=user_id,
            project_id=project_id,
            plugin_id=plugin_id,
        )

    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except PluginAlreadyInProjectError:
        raise PluginAlreadyInProjectHTTPException

    except PluginNotFoundError:
        raise PluginNotFoundHTTPException

    except PluginsLimitExceededError:
        raise PluginsLimitExceededHTTPException


@router.delete(
    '/projects/{project_id}/plugins/{plugin_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_plugin_from_project(
    project_id: int,
    plugin_id: int,
    plugin_service: PluginServiceDI,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        await plugin_service.remove_plugin_from_project(
            user_id=user_id,
            project_id=project_id,
            plugin_id=plugin_id,
        )

    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except PluginIsNotInProjectError:
        raise PluginIsNotInProjectHTTPException
