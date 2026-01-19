import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.apps.enums import KeyboardType
from src.apps.dialogues.schemas import DialogueReadSchema, DialogueWithBlocksReadSchema
from src.apps.plugins.schemas import PluginReadSchema


class ProjectReadSchema(BaseModel):
    project_id: int
    name: str = Field(max_length=256)
    user_id: UUID
    start_message: str = Field(max_length=4098)
    start_keyboard_type: KeyboardType
    created_at: datetime.datetime

    dialogues: list[DialogueReadSchema] = Field(default_factory=list)
    plugins: list[PluginReadSchema] = Field(default_factory=list)

    model_config = {
        'from_attributes': True,
    }


class ProjectToGenerateCodeReadSchema(ProjectReadSchema):
    dialogues: list[DialogueWithBlocksReadSchema] = Field(default_factory=list)


class ProjectCreateSchema(BaseModel):
    name: str = Field(max_length=256)
    start_message: str = Field(max_length=4098)
    start_keyboard_type: KeyboardType


class ProjectUpdateSchema(BaseModel):
    name: str = Field(max_length=256)
    start_message: str = Field(max_length=4098)
    start_keyboard_type: KeyboardType
