from typing import Annotated

from fastapi import Depends

from src.statistics.services import StatisticService

StatisticServiceDI = Annotated[StatisticService, Depends(StatisticService)]