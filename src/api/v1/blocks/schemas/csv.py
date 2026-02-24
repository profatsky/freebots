from typing import Union, Literal, Self

from pydantic import BaseModel, Field, field_validator

from src.api.v1.blocks.schemas.base import BlockReadSchema, BlockCreateSchema, BlockUpdateSchema
from src.apps.blocks.dto.csv import CSVBlockCreateDTO, CSVBlockReadDTO, CSVBlockUpdateDTO
from src.apps.enums import BlockType


class CSVBlockSchema(BaseModel):
    file_path: str = Field(max_length=256)
    data: dict[str, Union[int, str]]
    type: Literal[BlockType.CSV_BLOCK]

    @field_validator('data')
    @classmethod
    def check_data_length(cls, v: dict[str, Union[int, str]]) -> dict[str, Union[int, str]]:
        if len(v) > 25:
            raise ValueError('The length of the "data" field should not exceed 25')
        return v

    @property
    def is_draft(self) -> bool:
        return not (self.file_path and self.data)


class CSVBlockReadSchema(CSVBlockSchema, BlockReadSchema):
    @classmethod
    def from_dto(cls, dto: CSVBlockReadDTO) -> Self:
        return cls(
            block_id=dto.block_id,
            sequence_number=dto.sequence_number,
            type=dto.type,
            file_path=dto.file_path,
            data=dto.data,
        )


class CSVBlockCreateSchema(CSVBlockSchema, BlockCreateSchema):
    def to_dto(self) -> CSVBlockCreateDTO:
        return CSVBlockCreateDTO(type=self.type, file_path=self.file_path, data=self.data)


class CSVBlockUpdateSchema(CSVBlockSchema, BlockUpdateSchema):
    def to_dto(self) -> CSVBlockUpdateDTO:
        return CSVBlockUpdateDTO(type=self.type, file_path=self.file_path, data=self.data)
