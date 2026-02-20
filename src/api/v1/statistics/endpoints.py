from fastapi import APIRouter, Depends

from src.api.v1.users.exceptions import DontHavePermissionHTTPException
from src.apps.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.apps.statistics.dependencies.services_dependencies import StatisticServiceDI
from src.api.v1.statistics.schemas import StatisticReadSchema
from src.apps.users.errors import DontHavePermissionError

router = APIRouter(
    prefix='/statistics',
    tags=['Statistics'],
    dependencies=[Depends(access_token_required)],
)


@router.get('', response_model=StatisticReadSchema)
async def get_statistic(
    statistic_service: StatisticServiceDI,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        return await statistic_service.get_statistic(user_id)
    except DontHavePermissionError:
        raise DontHavePermissionHTTPException
