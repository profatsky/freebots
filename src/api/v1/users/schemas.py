from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel

from src.apps.users.dto import UserReadDTO


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

    @classmethod
    def from_dto(cls, user: UserReadDTO, project_count: int) -> Self:
        return UserWithStatsReadSchema(
            user_id=user.user_id,
            tg_id=user.tg_id,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            project_count=project_count,
        )
