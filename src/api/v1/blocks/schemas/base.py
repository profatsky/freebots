from typing import Self

from pydantic import BaseModel, Field

from src.apps.blocks.dto.base import BlockCreateDTO, BlockReadDTO, BlockUpdateDTO


class BlockReadSchema(BaseModel):
    block_id: int
    sequence_number: int = Field(ge=1)

    model_config = {
        'from_attributes': True,
    }

    @classmethod
    def from_dto(cls, dto: BlockReadDTO) -> Self:
        raise NotImplementedError


class BlockCreateSchema(BaseModel):
    def to_dto(self) -> BlockCreateDTO:
        raise NotImplementedError


class BlockUpdateSchema(BaseModel):
    def to_dto(self) -> BlockUpdateDTO:
        raise NotImplementedError
