from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.apps.enums import KeyboardType


@dataclass(frozen=True)
class ProjectCreateDTO:
    user_id: UUID
    name: str
    start_message: str
    start_keyboard_type: KeyboardType

    def __post_init__(self):
        self._validate_name()
        self._validate_start_message()

    def _validate_name(self):
        name_length = len(self.name)
        if name_length < 1 or name_length > 256:
            raise ValueError('Invalid project name')

    def _validate_start_message(self):
        if len(self.start_message) > 4098:
            raise ValueError('Invalid start message')


@dataclass(frozen=True)
class ProjectReadDTO(ProjectCreateDTO):
    project_id: int
    created_at: datetime


@dataclass(frozen=True)
class ProjectWithDialoguesAndPluginsReadDTO(ProjectReadDTO):
    # TODO: uncomment
    dialogues: list  # list[DialogueReadDTO]
    plugins: list  # list[PluginReadDTO]


@dataclass(frozen=True)
class ProjectUpdateDTO(ProjectCreateDTO):
    project_id: int
