from fastapi import APIRouter, Depends

from src.api.v1.users.exceptions import UnauthorizedHTTPException
from src.api.v1.users.schemas import UserWithStatsReadSchema
from src.apps.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.apps.projects.dependencies.services_dependencies import ProjectServiceDI
from src.apps.users.dependencies.services_dependencies import UserServiceDI
from src.apps.users.exceptions.services_exceptions import UserNotFoundError

router = APIRouter(
    prefix='/users',
    tags=['Auth'],
    dependencies=[Depends(access_token_required)],
)


@router.get(
    '/me',
    response_model=UserWithStatsReadSchema,
)
async def get_user(
    user_service: UserServiceDI,
    project_service: ProjectServiceDI,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        user = await user_service.get_user_by_id(user_id)
    except UserNotFoundError:
        raise UnauthorizedHTTPException

    project_count = await project_service.count_projects(user_id)

    return UserWithStatsReadSchema.from_dto(user=user, project_count=project_count)
