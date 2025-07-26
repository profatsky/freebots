import datetime

from sqlalchemy import String, DateTime, func, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.sessions import Base
from src.apps.enums import TriggerEventType


class DialogueModel(Base):
    __tablename__ = 'dialogues'

    dialogue_id: Mapped[int] = mapped_column(primary_key=True)

    trigger_id: Mapped[int] = mapped_column(ForeignKey('triggers.trigger_id', ondelete='RESTRICT'))
    trigger: Mapped['TriggerModel'] = relationship(back_populates='dialogue')

    project_id: Mapped[int] = mapped_column(ForeignKey('projects.project_id', ondelete='CASCADE'), nullable=True)
    project: Mapped['ProjectModel'] = relationship(back_populates='dialogues')

    blocks: Mapped[list['BlockModel']] = relationship(back_populates='dialogue')

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    template: Mapped['DialogueTemplateModel'] = relationship(back_populates='dialogue')


class TriggerModel(Base):
    __tablename__ = 'triggers'

    trigger_id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[TriggerEventType] = mapped_column(Enum(TriggerEventType).values_callable, nullable=False)
    value: Mapped[str] = mapped_column(String(64))

    dialogue: Mapped[DialogueModel] = relationship(back_populates='trigger')
