from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class SubscriptionTariff(StrEnum):
    PRO = 'pro'


class SubscriptionReadSchema(BaseModel):
    subscription_id: UUID
    tariff: SubscriptionTariff
    expires_at: datetime
    created_at: datetime
    user_id: UUID

    model_config = {
        'from_attributes': True,
    }


class SubscriptionCreateSchema(BaseModel):
    tariff: SubscriptionTariff = SubscriptionTariff.PRO
    duration_days: int = Field(gt=0)
