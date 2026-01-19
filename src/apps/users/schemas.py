from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserReadSchema(BaseModel):
    user_id: UUID
    tg_id: int
    is_superuser: bool
    created_at: datetime

    model_config = {
        'from_attributes': True,
    }


class UserWithStatsReadSchema(UserReadSchema):
    project_count: int
