from fastapi import APIRouter, Depends

from src.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.statistics.dependencies.services_dependencies import StatisticServiceDI
from src.statistics.schemas import StatisticSchema
from src.users.exceptions.http_exceptions import DontHavePermissionHTTPException
from src.users.exceptions.services_exceptions import DontHavePermissionError

router = APIRouter(
    prefix='/statistics',
    tags=['Statistics'],
    dependencies=[Depends(access_token_required)],
)


# TODO: admin privileges require
@router.get('', response_model=StatisticSchema)
async def get_statistic(
    statistic_service: StatisticServiceDI,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        return await statistic_service.get_statistic(user_id)
    except DontHavePermissionError:
        raise DontHavePermissionHTTPException
