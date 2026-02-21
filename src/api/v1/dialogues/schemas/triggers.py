from typing import Self

from pydantic import BaseModel, Field

from src.apps.dialogues.dto import DialogueTriggerReadDTO, DialogueTriggerCreateDTO, DialogueTriggerUpdateDTO
from src.apps.enums import TriggerEventType


class DialogueTriggerCreateSchema(BaseModel):
    event_type: TriggerEventType
    value: str = Field(max_length=64)

    def to_dto(self) -> DialogueTriggerCreateDTO:
        return DialogueTriggerCreateDTO(
            event_type=self.event_type,
            value=self.value,
        )


class DialogueTriggerReadSchema(BaseModel):
    trigger_id: int
    event_type: TriggerEventType
    value: str = Field(max_length=64)

    model_config = {
        'from_attributes': True,
    }

    @classmethod
    def from_dto(cls, dto: DialogueTriggerReadDTO) -> Self:
        return cls(
            trigger_id=dto.trigger_id,
            event_type=dto.event_type,
            value=dto.value,
        )


class DialogueTriggerUpdateSchema(DialogueTriggerCreateSchema):
    def to_dto(self) -> DialogueTriggerUpdateDTO:
        return DialogueTriggerUpdateDTO(
            event_type=self.event_type,
            value=self.value,
        )
