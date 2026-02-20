from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.payments.models import PaymentModel
from src.apps.users.dto import UserReadDTO
from src.infrastructure.db.sessions import Base


class UserModel(Base):
    __tablename__ = 'users'

    user_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    tg_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
    )
    is_superuser: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    projects: Mapped[list['ProjectModel']] = relationship(back_populates='user')
    subscriptions: Mapped[list['SubscriptionModel']] = relationship(back_populates='user')
    payments: Mapped[list[PaymentModel]] = relationship(back_populates='user')

    def to_dto(self) -> UserReadDTO:
        return UserReadDTO(
            user_id=self.user_id,
            tg_id=self.tg_id,
            is_superuser=self.is_superuser,
            created_at=self.created_at,
        )
