from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy import select, delete

from src.core.base_repository import BaseRepository
from src.apps.subscriptions.models import SubscriptionModel
from src.apps.subscriptions.schemas import SubscriptionReadSchema, SubscriptionCreateSchema


class SubscriptionRepository(BaseRepository):
    async def create_subscription(
        self,
        user_id: UUID,
        subscription_data: SubscriptionCreateSchema,
    ) -> SubscriptionReadSchema:
        expires_at = datetime.now() + timedelta(days=subscription_data.duration_days)

        subscription = SubscriptionModel(
            user_id=user_id,
            tariff=subscription_data.tariff,
            expires_at=expires_at,
        )

        self._session.add(subscription)
        await self._session.commit()

        return SubscriptionReadSchema.model_validate(subscription)

    async def get_subscriptions(self, user_id: UUID) -> list[SubscriptionReadSchema]:
        result = await self._session.execute(
            select(SubscriptionModel)
            .where(SubscriptionModel.user_id == user_id)
            .order_by(SubscriptionModel.created_at.desc())
        )
        subscriptions = result.scalars().all()
        return [SubscriptionReadSchema.model_validate(sub) for sub in subscriptions]

    async def get_active_subscription(self, user_id: UUID) -> Optional[SubscriptionReadSchema]:
        result = await self._session.execute(
            select(SubscriptionModel)
            .where(
                SubscriptionModel.user_id == user_id,
                SubscriptionModel.expires_at > datetime.now(),
            )
            .order_by(SubscriptionModel.expires_at.desc())
        )
        subscription = result.scalar()

        if subscription is None:
            return None

        return SubscriptionReadSchema.model_validate(subscription)

    async def delete_subscription(self, subscription_id: UUID):
        await self._session.execute(
            delete(SubscriptionModel).where(SubscriptionModel.subscription_id == subscription_id)
        )
        await self._session.commit()
