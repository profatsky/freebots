import datetime

from pydantic import BaseModel, EmailStr


class UserReadSchema(BaseModel):
    user_id: int
    email: EmailStr
    registered_at: datetime.datetime
    is_superuser: bool

    model_config = {
        'from_attributes': True,
    }


class UserWithStatsReadSchema(UserReadSchema):
    project_count: int
