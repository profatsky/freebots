from typing import Annotated

from fastapi import APIRouter, Query, status, Body, Depends

from src.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.plugins.dependencies.services_dependencies import PluginServiceDI
from src.plugins.exceptions.http_exceptions import (
    PluginNotFoundHTTPException,
    PluginAlreadyInProjectHTTPException,
    PluginIsNotInProjectHTTPException,
)
from src.plugins.exceptions.services_exceptions import (
    PluginNotFoundError,
    PluginAlreadyInProjectError,
    PluginIsNotInProjectError,
)
from src.plugins.schemas import PluginReadSchema
from src.projects.exceptions.http_exceptions import ProjectNotFoundHTTPException, NoPermissionForProjectHTTPException
from src.projects.exceptions.services_exceptions import ProjectNotFoundError, NoPermissionForProjectError

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
