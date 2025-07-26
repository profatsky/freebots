from typing import Annotated

from fastapi import Depends

from src.apps.statistics.repositories import StatisticRepository

StatisticRepositoryDI = Annotated[StatisticRepository, Depends(StatisticRepository)]
