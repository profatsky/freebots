from typing import Union, Literal, Self

from pydantic import BaseModel, Field, field_validator

from src.api.v1.blocks.schemas.base import BlockReadSchema, BlockCreateSchema, BlockUpdateSchema
from src.apps.blocks.dto.excel import ExcelBlockCreateDTO, ExcelBlockReadDTO, ExcelBlockUpdateDTO
from src.apps.enums import BlockType


class ExcelBlockSchema(BaseModel):
    file_path: str = Field(max_length=256)
    data: dict[str, Union[int, str]]
    type: Literal[BlockType.EXCEL_BLOCK.value]

    @field_validator('data')
    @classmethod
    def check_data_length(cls, v: dict[str, Union[int, str]]) -> dict[str, Union[int, str]]:
        if len(v) > 25:
            raise ValueError('The length of the "data" field should not exceed 25')
        return v

    @property
    def is_draft(self) -> bool:
        return not (self.file_path and self.data)


class ExcelBlockReadSchema(ExcelBlockSchema, BlockReadSchema):
    @classmethod
    def from_dto(cls, dto: ExcelBlockReadDTO) -> Self:
        return cls(
            block_id=dto.block_id,
            sequence_number=dto.sequence_number,
            type=dto.type,
            file_path=dto.file_path,
            data=dto.data,
        )


class ExcelBlockCreateSchema(ExcelBlockSchema, BlockCreateSchema):
    def to_dto(self) -> ExcelBlockCreateDTO:
        return ExcelBlockCreateDTO(
            type=self.type,
            file_path=self.file_path,
            data=self.data,
        )


class ExcelBlockUpdateSchema(ExcelBlockSchema, BlockUpdateSchema):
    def to_dto(self) -> ExcelBlockUpdateDTO:
        return ExcelBlockUpdateDTO(
            type=self.type,
            file_path=self.file_path,
            data=self.data,
        )
