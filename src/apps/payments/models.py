from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, DateTime, func, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.payments.enums import PaymentStatus
from src.infrastructure.db.sessions import Base


class PaymentModel(Base):
    __tablename__ = 'payments'

    payment_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    yookassa_payment_id: Mapped[UUID] = mapped_column()
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus).values_callable, nullable=False)
    confirmation_url: Mapped[str] = mapped_column(String(2048))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    subscription_id: Mapped[UUID] = mapped_column(
        ForeignKey('subscriptions.subscription_id', ondelete='SET NULL'),
        nullable=True,
    )
    subscription: Mapped['SubscriptionModel'] = relationship(back_populates='payment')

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))
    user: Mapped['UserModel'] = relationship(back_populates='payments')
