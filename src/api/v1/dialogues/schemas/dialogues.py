from datetime import datetime
from typing import Self

from pydantic import BaseModel, field_validator

from src.api.v1.blocks.schemas.base import BlockReadSchema
from src.api.v1.dialogues.schemas.triggers import DialogueTriggerCreateSchema, DialogueTriggerReadSchema
from src.apps.blocks import utils
from src.apps.dialogues.dto import DialogueCreateDTO, DialogueReadDTO


class DialogueCreateSchema(BaseModel):
    trigger: DialogueTriggerCreateSchema

    def to_dto(self, project_id: int) -> DialogueCreateDTO:
        return DialogueCreateDTO(
            project_id=project_id,
            trigger=self.trigger.to_dto(),
        )


class DialogueReadSchema(BaseModel):
    dialogue_id: int
    trigger: DialogueTriggerReadSchema
    created_at: datetime

    model_config = {
        'from_attributes': True,
    }

    @classmethod
    def from_dto(cls, dto: DialogueReadDTO) -> Self:
        return cls(
            dialogue_id=dto.dialogue_id,
            trigger=DialogueTriggerReadSchema.from_dto(dto.trigger),
            created_at=dto.created_at,
        )


class DialogueWithBlocksReadSchema(DialogueReadSchema):
    blocks: list[BlockReadSchema]

    @field_validator('blocks')
    @classmethod
    def transform_blocks(cls, blocks_to_transform):
        return [utils.validate_block_from_db(block) for block in blocks_to_transform]
