import datetime
from typing import Self

from sqlalchemy import String, DateTime, func, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.dialogues.dto import DialogueCreateDTO, DialogueTriggerCreateDTO, DialogueReadDTO, DialogueTriggerReadDTO
from src.infrastructure.db.sessions import Base
from src.apps.enums import TriggerEventType


class DialogueModel(Base):
    __tablename__ = 'dialogues'

    dialogue_id: Mapped[int] = mapped_column(primary_key=True)

    trigger_id: Mapped[int] = mapped_column(ForeignKey('triggers.trigger_id', ondelete='RESTRICT'))
    trigger: Mapped['DialogueTriggerModel'] = relationship(back_populates='dialogue')

    project_id: Mapped[int] = mapped_column(ForeignKey('projects.project_id', ondelete='CASCADE'), nullable=True)
    project: Mapped['ProjectModel'] = relationship(back_populates='dialogues')

    blocks: Mapped[list['BlockModel']] = relationship(back_populates='dialogue')

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    template: Mapped['DialogueTemplateModel'] = relationship(back_populates='dialogue')

    @classmethod
    def from_dto(cls, dto: DialogueCreateDTO) -> Self:
        return cls(
            project_id=dto.project_id,
            trigger=DialogueTriggerModel.from_dto(dto.trigger),
        )

    def to_dto(self) -> DialogueReadDTO:
        return DialogueReadDTO(
            dialogue_id=self.dialogue_id,
            trigger=self.trigger.to_dto(),
            project_id=self.project_id,
            created_at=self.created_at,
        )


class DialogueTriggerModel(Base):
    __tablename__ = 'triggers'

    trigger_id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[TriggerEventType] = mapped_column(Enum(TriggerEventType).values_callable, nullable=False)
    value: Mapped[str] = mapped_column(String(64))

    dialogue: Mapped[DialogueModel] = relationship(back_populates='trigger')

    @classmethod
    def from_dto(cls, dto: DialogueTriggerCreateDTO) -> Self:
        return cls(
            event_type=dto.event_type,
            value=dto.value,
        )

    def to_dto(self) -> DialogueTriggerReadDTO:
        return DialogueTriggerReadDTO(
            trigger_id=self.trigger_id,
            event_type=self.event_type,
            value=self.value,
        )
