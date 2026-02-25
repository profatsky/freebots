import datetime
from pathlib import Path
from typing import Self

from pydantic import BaseModel, Field

from src.apps.enums import TriggerEventType
from src.apps.plugins.dto import PluginReadDTO, PluginTriggerReadDTO


class PluginTriggerCreateSchema(BaseModel):
    event_type: TriggerEventType
    value: str = Field(max_length=64)
    is_admin: bool


class PluginTriggerReadSchema(BaseModel):
    trigger_id: int
    event_type: TriggerEventType
    value: str = Field(max_length=64)
    is_admin: bool

    model_config = {
        'from_attributes': True,
    }

    @classmethod
    def from_dto(cls, dto: PluginTriggerReadDTO) -> Self:
        return cls(
            trigger_id=dto.trigger_id,
            event_type=dto.event_type,
            value=dto.value,
            is_admin=dto.is_admin,
        )


class PluginReadSchema(BaseModel):
    plugin_id: int
    name: str
    summary: str
    image_path: str
    created_at: datetime.datetime
    handlers_file_path: str
    db_funcs_file_path: str
    triggers: list[PluginTriggerReadSchema]
    readme_file_path: str

    model_config = {
        'from_attributes': True,
    }

    @classmethod
    def from_dto(cls, dto: PluginReadDTO) -> Self:
        triggers = [PluginTriggerReadSchema.from_dto(trigger) for trigger in dto.triggers]
        return cls(
            plugin_id=dto.plugin_id,
            name=dto.name,
            summary=dto.summary,
            image_path=dto.image_path,
            created_at=dto.created_at,
            handlers_file_path=dto.handlers_file_path,
            db_funcs_file_path=dto.db_funcs_file_path,
            triggers=triggers,
            readme_file_path=dto.readme_file_path,
        )


# TODO: move to dto
class PluginCreateSchema(BaseModel):
    name: str
    summary: str
    image_path: Path
    handlers_file_path: Path
    db_funcs_file_path: Path
    readme_file_path: Path
    triggers: list[PluginTriggerCreateSchema] = []
