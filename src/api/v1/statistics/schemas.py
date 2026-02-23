from typing import Self

from pydantic import BaseModel

from src.apps.statistics.dto import StatisticReadDTO


class StatisticReadSchema(BaseModel):
    user_count: int
    project_count: int

    @classmethod
    def from_dto(cls, dto: StatisticReadDTO) -> Self:
        return StatisticReadSchema(
            user_count=dto.user_count,
            project_count=dto.project_count,
        )
