from typing import Optional
from uuid import UUID

from src.apps.subscriptions.dependencies.repositories_dependencies import SubscriptionRepositoryDI
from src.apps.subscriptions.schemas import SubscriptionReadSchema, SubscriptionCreateSchema
from src.apps.subscriptions.exceptions.services_exceptions import SubscriptionAlreadyExistsError
from src.apps.users.dependencies.services_dependencies import UserServiceDI


class SubscriptionService:
    def __init__(
        self,
        subscription_repository: SubscriptionRepositoryDI,
        user_service: UserServiceDI,
    ):
        self._subscription_repository = subscription_repository
        self._user_service = user_service

    async def create_subscription(
        self,
        user_id: UUID,
        subscription: SubscriptionCreateSchema,
    ) -> SubscriptionReadSchema:
        active_subscription = await self.get_active_subscription(user_id)
        if active_subscription is not None:
            raise SubscriptionAlreadyExistsError
        return await self._subscription_repository.create_subscription(user_id, subscription)

    async def get_active_subscription(self, user_id: UUID) -> Optional[SubscriptionReadSchema]:
        await self._user_service.raise_error_if_not_exists(user_id)
        return await self._subscription_repository.get_active_subscription(user_id)

    async def get_subscriptions(self, user_id: UUID) -> list[SubscriptionReadSchema]:
        await self._user_service.raise_error_if_not_exists(user_id)
        return await self._subscription_repository.get_subscriptions(user_id)
