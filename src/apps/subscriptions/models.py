from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.subscriptions.schemas import SubscriptionTariff
from src.infrastructure.db.sessions import Base


class SubscriptionModel(Base):
    __tablename__ = 'subscriptions'

    subscription_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    tariff: Mapped[SubscriptionTariff] = mapped_column(Enum(SubscriptionTariff).values_callable, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))
    user: Mapped['UserModel'] = relationship(back_populates='subscriptions')

    payment: Mapped['PaymentModel'] = relationship(back_populates='subscription')
