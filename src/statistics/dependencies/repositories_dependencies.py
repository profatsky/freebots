from typing import Annotated

from fastapi import Depends

from src.statistics.repositories import StatisticRepository

StatisticRepositoryDI = Annotated[StatisticRepository, Depends(StatisticRepository)]
