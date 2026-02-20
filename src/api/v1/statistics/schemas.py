from pydantic import BaseModel


class StatisticReadSchema(BaseModel):
    user_count: int
    project_count: int
