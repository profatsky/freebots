from dataclasses import dataclass
from datetime import datetime

from src.apps.enums import TriggerEventType


@dataclass(frozen=True)
class DialogueTriggerCreateDTO:
    event_type: TriggerEventType
    value: str

    def __post_init__(self):
        self._validate_value()

    def _validate_value(self):
        if len(self.value) > 64:
            raise ValueError('Invalid value')


@dataclass(frozen=True)
class DialogueTriggerReadDTO(DialogueTriggerCreateDTO):
    trigger_id: int


@dataclass(frozen=True)
class DialogueTriggerUpdateDTO(DialogueTriggerCreateDTO):
    pass


@dataclass(frozen=True)
class DialogueCreateDTO:
    project_id: int
    trigger: DialogueTriggerCreateDTO


@dataclass(frozen=True)
class DialogueReadDTO(DialogueCreateDTO):
    dialogue_id: int
    trigger: DialogueTriggerReadDTO
    created_at: datetime
