from fastapi import APIRouter, status, Depends

from src.apps.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.apps.projects.dependencies.services_dependencies import ProjectServiceDI
from src.api.v1.projects.exceptions import (
    ProjectNotFoundHTTPException,
    NoPermissionForProjectHTTPException,
    ProjectsLimitExceededHTTPException,
)
from src.apps.projects.errors import (
    ProjectsLimitExceededError,
    ProjectNotFoundError,
    NoPermissionForProjectError,
)
from src.api.v1.projects.schemas import (
    ProjectCreateSchema,
    ProjectUpdateSchema,
    ProjectReadSchema,
    ProjectWithDialoguesAndPluginsReadSchema,
)

router = APIRouter(
    prefix='/projects',
    tags=['Projects'],
    dependencies=[Depends(access_token_required)],
)


@router.post('', response_model=ProjectReadSchema, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_service: ProjectServiceDI,
    project: ProjectCreateSchema,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        project = await project_service.create_project(project.to_dto(user_id=user_id))
    except ProjectsLimitExceededError:
        raise ProjectsLimitExceededHTTPException
    return ProjectReadSchema.from_dto(project)


@router.get('', response_model=list[ProjectWithDialoguesAndPluginsReadSchema])
async def get_projects_with_dialogues_and_plugins(
    project_service: ProjectServiceDI,
    user_id: UserIDFromAccessTokenDI,
):
    projects = await project_service.get_projects_with_dialogues_and_plugins(user_id)
    return [ProjectWithDialoguesAndPluginsReadSchema.from_dto(project) for project in projects]


@router.put('/{project_id}', response_model=ProjectReadSchema)
async def update_project(
    project_service: ProjectServiceDI,
    project_id: int,
    project: ProjectUpdateSchema,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        project = await project_service.update_project(project.to_dto(project_id=project_id, user_id=user_id))
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException
    return ProjectReadSchema.from_dto(project)


@router.delete('/{project_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_service: ProjectServiceDI,
    project_id: int,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        await project_service.delete_project(
            user_id=user_id,
            project_id=project_id,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException
