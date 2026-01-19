import datetime

from pydantic import BaseModel, Field

from src.apps.enums import TriggerEventType


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


class PluginCreateSchema(BaseModel):
    name: str
    summary: str
    image_path: str
    handlers_file_path: str
    db_funcs_file_path: str
    readme_file_path: str
    triggers: list[PluginTriggerCreateSchema] = []
