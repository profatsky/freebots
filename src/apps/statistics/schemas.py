from pydantic import BaseModel


class StatisticSchema(BaseModel):
    user_count: int
    project_count: int
