from dataclasses import dataclass
from datetime import datetime

from src.apps.enums import TriggerEventType


@dataclass(frozen=True)
class PluginTriggerReadDTO:
    trigger_id: int
    event_type: TriggerEventType
    value: str
    is_admin: bool

    def __post_init__(self):
        self._validate_value()

    def _validate_value(self):
        if len(self.value) > 64:
            raise ValueError('Invalid value')


# TODO: add field validation
@dataclass(frozen=True)
class PluginReadDTO:
    plugin_id: int
    name: str
    summary: str
    image_path: str
    created_at: datetime
    handlers_file_path: str
    db_funcs_file_path: str
    triggers: list[PluginTriggerReadDTO]
    readme_file_path: str
