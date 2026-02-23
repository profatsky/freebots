from typing import Literal, Self

from pydantic import BaseModel, Field

from src.api.v1.blocks.schemas.base import BlockReadSchema, BlockCreateSchema, BlockUpdateSchema
from src.apps.blocks.dto.image import ImageBlockCreateDTO, ImageBlockReadDTO, ImageBlockUpdateDTO
from src.apps.enums import BlockType


class BaseImageBlockSchema(BaseModel):
    image_path: str = Field(max_length=256)
    type: Literal[BlockType.IMAGE_BLOCK.value]

    @property
    def is_draft(self) -> bool:
        return not bool(self.image_path)


class ImageBlockReadSchema(BaseImageBlockSchema, BlockReadSchema):
    @classmethod
    def from_dto(cls, dto: ImageBlockReadDTO) -> Self:
        return cls(
            block_id=dto.block_id,
            sequence_number=dto.sequence_number,
            type=dto.type,
            image_path=dto.image_path,
        )


class ImageBlockCreateSchema(BaseImageBlockSchema, BlockCreateSchema):
    def to_dto(self) -> ImageBlockCreateDTO:
        return ImageBlockCreateDTO(
            type=self.type,
            image_path=self.image_path,
        )


class ImageBlockUpdateSchema(BaseImageBlockSchema, BlockUpdateSchema):
    def to_dto(self) -> ImageBlockUpdateDTO:
        return ImageBlockUpdateDTO(
            type=self.type,
            image_path=self.image_path,
        )
