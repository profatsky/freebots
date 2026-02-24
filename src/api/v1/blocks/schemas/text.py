from typing import Literal, Self

from pydantic import BaseModel, Field

from src.api.v1.blocks.schemas.base import BlockReadSchema, BlockCreateSchema, BlockUpdateSchema
from src.apps.blocks.dto.text import TextBlockCreateDTO, TextBlockReadDTO, TextBlockUpdateDTO
from src.apps.enums import BlockType


class BaseTextBlockSchema(BaseModel):
    message_text: str = Field(max_length=4096)
    type: Literal[BlockType.TEXT_BLOCK]

    @property
    def is_draft(self) -> bool:
        return not bool(self.message_text)


class TextBlockReadSchema(BaseTextBlockSchema, BlockReadSchema):
    @classmethod
    def from_dto(cls, dto: TextBlockReadDTO) -> Self:
        return cls(
            block_id=dto.block_id,
            sequence_number=dto.sequence_number,
            type=dto.type,
            message_text=dto.message_text,
        )


class TextBlockCreateSchema(BaseTextBlockSchema, BlockCreateSchema):
    def to_dto(self) -> TextBlockCreateDTO:
        return TextBlockCreateDTO(
            type=self.type,
            message_text=self.message_text,
        )


class TextBlockUpdateSchema(BaseTextBlockSchema, BlockUpdateSchema):
    def to_dto(self) -> TextBlockUpdateDTO:
        return TextBlockUpdateDTO(
            type=self.type,
            message_text=self.message_text,
        )
