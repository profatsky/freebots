from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class UserReadDTO:
    user_id: UUID
    tg_id: int
    is_superuser: bool
    created_at: datetime
