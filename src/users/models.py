import datetime

from sqlalchemy import DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.sessions import Base


class UserModel(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(String(254), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(256))

    is_superuser: Mapped[bool] = mapped_column(default=False)

    registered_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    projects: Mapped[list['ProjectModel']] = relationship(back_populates='user')
