from typing import Annotated

from fastapi import Depends

from src.apps.statistics.services import StatisticService

StatisticServiceDI = Annotated[StatisticService, Depends(StatisticService)]
