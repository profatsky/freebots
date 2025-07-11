from fastapi import APIRouter, Depends

from src.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.users.dependencies.services_dependencies import UserServiceDI
from src.users.exceptions.http_exceptions import UnauthorizedHTTPException
from src.users.exceptions.services_exceptions import UserNotFoundError
from src.users.schemas import UserWithStatsReadSchema

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
        user_id: UserIDFromAccessTokenDI,
):
    try:
        return await user_service.get_user_with_stats(user_id)
    except UserNotFoundError:
        raise UnauthorizedHTTPException
