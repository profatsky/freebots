from typing import Annotated

from fastapi import Depends

from src.apps.subscriptions.repositories import SubscriptionRepository

SubscriptionRepositoryDI = Annotated[SubscriptionRepository, Depends(SubscriptionRepository)]
