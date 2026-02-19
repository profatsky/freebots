from typing import Optional
from uuid import UUID

from fastapi import APIRouter, status, Depends

from src.api.v1.users.exceptions import UserNotFoundHTTPException, DontHavePermissionHTTPException
from src.apps.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.apps.subscriptions.dependencies.services_dependencies import SubscriptionServiceDI
from src.apps.subscriptions.exceptions.http_exceptions import (
    SubscriptionAlreadyExistsHTTPException,
)
from src.apps.subscriptions.exceptions.services_exceptions import SubscriptionAlreadyExistsError
from src.apps.subscriptions.schemas import SubscriptionReadSchema, SubscriptionCreateSchema
from src.apps.users.dependencies.services_dependencies import UserServiceDI
from src.apps.users.errors import UserNotFoundError, DontHavePermissionError


router = APIRouter(
    prefix='/users/{user_id}/subscriptions',
    tags=['Subscriptions'],
    dependencies=[Depends(access_token_required)],
)


async def check_access_permissions(
    user_id: UUID,
    current_user_id: UserIDFromAccessTokenDI,
    user_service: UserServiceDI,
):
    if user_id != current_user_id:
        current_user = await user_service.get_user_by_id(current_user_id)
        if not current_user.is_superuser:
            raise DontHavePermissionError


async def check_superuser_permissions(
    current_user_id: UserIDFromAccessTokenDI,
    user_service: UserServiceDI,
):
    current_user = await user_service.get_user_by_id(current_user_id)
    if not current_user.is_superuser:
        raise DontHavePermissionError


@router.get(
    '',
    response_model=list[SubscriptionReadSchema],
)
async def get_subscriptions(
    user_id: UUID,
    subscription_service: SubscriptionServiceDI,
    user_service: UserServiceDI,
    current_user_id: UserIDFromAccessTokenDI,
):
    try:
        await check_access_permissions(user_id, current_user_id, user_service)
        return await subscription_service.get_subscriptions(user_id)

    except UserNotFoundError:
        raise UserNotFoundHTTPException

    except DontHavePermissionError:
        raise DontHavePermissionHTTPException


@router.get(
    '/active',
    response_model=Optional[SubscriptionReadSchema],
)
async def get_active_subscription(
    user_id: UUID,
    subscription_service: SubscriptionServiceDI,
    user_service: UserServiceDI,
    current_user_id: UserIDFromAccessTokenDI,
):
    try:
        await check_access_permissions(user_id, current_user_id, user_service)
        return await subscription_service.get_active_subscription(user_id)

    except UserNotFoundError:
        raise UserNotFoundHTTPException

    except DontHavePermissionError:
        raise DontHavePermissionHTTPException


@router.post(
    '',
    response_model=SubscriptionReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_subscription(
    user_id: UUID,
    subscription_data: SubscriptionCreateSchema,
    subscription_service: SubscriptionServiceDI,
    user_service: UserServiceDI,
    current_user_id: UserIDFromAccessTokenDI,
):
    try:
        await check_superuser_permissions(current_user_id, user_service)
        return await subscription_service.create_subscription(user_id, subscription_data)

    except UserNotFoundError:
        raise UserNotFoundHTTPException

    except DontHavePermissionError:
        raise DontHavePermissionHTTPException

    except SubscriptionAlreadyExistsError:
        raise SubscriptionAlreadyExistsHTTPException
