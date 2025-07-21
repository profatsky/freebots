from fastapi import APIRouter, status, Depends

from src.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.projects.dependencies.services_dependencies import ProjectServiceDI
from src.projects.exceptions.http_exceptions import (
    ProjectNotFoundHTTPException,
    NoPermissionForProjectHTTPException,
    ProjectsLimitExceededHTTPException,
)
from src.projects.exceptions.services_exceptions import (
    ProjectsLimitExceededError,
    ProjectNotFoundError,
    NoPermissionForProjectError,
)
from src.projects.schemas import ProjectCreateSchema, ProjectUpdateSchema, ProjectReadSchema

router = APIRouter(
    prefix='/projects',
    tags=['Projects'],
    dependencies=[Depends(access_token_required)],
)


@router.post(
    '',
    response_model=ProjectReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    project_data: ProjectCreateSchema,
    project_service: ProjectServiceDI,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        return await project_service.create_project(
            user_id=user_id,
            project_data=project_data,
        )
    except ProjectsLimitExceededError:
        raise ProjectsLimitExceededHTTPException


@router.get(
    '',
    response_model=list[ProjectReadSchema],
)
async def get_projects(
    project_service: ProjectServiceDI,
    user_id: UserIDFromAccessTokenDI,
):
    return await project_service.get_projects(user_id)


@router.put(
    '/{project_id}',
    response_model=ProjectReadSchema,
)
async def update_project(
    project_id: int,
    project_data: ProjectUpdateSchema,
    project_service: ProjectServiceDI,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        return await project_service.update_project(
            user_id=user_id,
            project_id=project_id,
            project_data=project_data,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException


@router.delete(
    '/{project_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: int,
    project_service: ProjectServiceDI,
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
