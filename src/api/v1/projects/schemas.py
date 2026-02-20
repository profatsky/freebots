import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, Field

from src.apps.enums import KeyboardType
from src.apps.dialogues.schemas import DialogueReadSchema, DialogueWithBlocksReadSchema
from src.apps.plugins.schemas import PluginReadSchema
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
    def from_dto(cls, project: ProjectReadDTO) -> Self:
        return ProjectReadSchema(
            project_id=project.project_id,
            name=project.name,
            user_id=project.user_id,
            start_message=project.start_message,
            start_keyboard_type=project.start_keyboard_type,
            created_at=project.created_at,
        )


class ProjectWithDialoguesAndPluginsReadSchema(ProjectReadSchema):
    dialogues: list[DialogueReadSchema] = Field(default_factory=list)
    plugins: list[PluginReadSchema] = Field(default_factory=list)

    @classmethod
    def from_dto(cls, project: ProjectWithDialoguesAndPluginsReadDTO) -> Self:
        return ProjectWithDialoguesAndPluginsReadSchema(
            project_id=project.project_id,
            name=project.name,
            user_id=project.user_id,
            start_message=project.start_message,
            start_keyboard_type=project.start_keyboard_type,
            created_at=project.created_at,
            dialogues=project.dialogues,
            plugins=project.plugins,
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
