import datetime

from pydantic import BaseModel, field_validator, Field

from src.apps.enums import TriggerEventType
from src.apps.blocks.schemas import UnionBlockReadSchema
from src.apps.blocks import utils


class DialogueCreateSchema(BaseModel):
    trigger: 'TriggerCreateSchema'


class DialogueReadSchema(BaseModel):
    dialogue_id: int
    trigger: 'TriggerReadSchema'
    created_at: datetime.datetime

    model_config = {
        'from_attributes': True,
    }


class TriggerCreateSchema(BaseModel):
    event_type: TriggerEventType
    value: str = Field(max_length=64)


class TriggerUpdateSchema(TriggerCreateSchema):
    pass


class TriggerReadSchema(BaseModel):
    trigger_id: int
    event_type: TriggerEventType
    value: str = Field(max_length=64)

    model_config = {
        'from_attributes': True,
    }


class DialogueWithBlocksReadSchema(DialogueReadSchema):
    blocks: list[UnionBlockReadSchema]

    @field_validator('blocks')
    @classmethod
    def transform_blocks(cls, blocks_to_transform):
        return [utils.validate_block_from_db(block) for block in blocks_to_transform]
