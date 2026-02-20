from dataclasses import dataclass


@dataclass(frozen=True)
class StatisticReadDTO:
    user_count: int
    project_count: int
