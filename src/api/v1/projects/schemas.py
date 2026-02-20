import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, Field

from src.apps.enums import KeyboardType
from src.apps.dialogues.schemas import DialogueReadSchema, DialogueWithBlocksReadSchema
from src.api.v1.plugins.schemas import PluginReadSchema
from src.apps.projects.dto import (
    ProjectCreateDTO,
    ProjectReadDTO,
    ProjectWithDialoguesAndPluginsReadDTO,
    ProjectUpdateDTO,
)


class ProjectReadSchema(BaseModel):
    project_id: int
    user_id: UUID
    name: str = Field(min_length=1, max_length=256)
    start_message: str = Field(max_length=4098)
    start_keyboard_type: KeyboardType
    created_at: datetime.datetime

    model_config = {
        'from_attributes': True,
    }

    @classmethod
    def from_dto(cls, dto: ProjectReadDTO) -> Self:
        return cls(
            project_id=dto.project_id,
            name=dto.name,
            user_id=dto.user_id,
            start_message=dto.start_message,
            start_keyboard_type=dto.start_keyboard_type,
            created_at=dto.created_at,
        )


class ProjectWithDialoguesAndPluginsReadSchema(ProjectReadSchema):
    dialogues: list[DialogueReadSchema] = Field(default_factory=list)
    plugins: list[PluginReadSchema] = Field(default_factory=list)

    @classmethod
    def from_dto(cls, dto: ProjectWithDialoguesAndPluginsReadDTO) -> Self:
        return cls(
            project_id=dto.project_id,
            name=dto.name,
            user_id=dto.user_id,
            start_message=dto.start_message,
            start_keyboard_type=dto.start_keyboard_type,
            created_at=dto.created_at,
            dialogues=dto.dialogues,
            plugins=dto.plugins,
        )


class ProjectToGenerateCodeReadSchema(ProjectReadSchema):
    dialogues: list[DialogueWithBlocksReadSchema] = Field(default_factory=list)


class ProjectCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=256)
    start_message: str = Field(min_length=1, max_length=4098)
    start_keyboard_type: KeyboardType

    def to_dto(self, user_id: UUID) -> ProjectCreateDTO:
        return ProjectCreateDTO(
            user_id=user_id,
            name=self.name,
            start_message=self.start_message,
            start_keyboard_type=self.start_keyboard_type,
        )


class ProjectUpdateSchema(BaseModel):
    name: str = Field(max_length=256)
    start_message: str = Field(max_length=4098)
    start_keyboard_type: KeyboardType

    def to_dto(self, project_id: int, user_id: UUID) -> ProjectUpdateDTO:
        return ProjectUpdateDTO(
            project_id=project_id,
            user_id=user_id,
            name=self.name,
            start_message=self.start_message,
            start_keyboard_type=self.start_keyboard_type,
        )
