from typing import Annotated

from fastapi import Depends

from src.apps.subscriptions.services import SubscriptionService

SubscriptionServiceDI = Annotated[SubscriptionService, Depends(SubscriptionService)]
