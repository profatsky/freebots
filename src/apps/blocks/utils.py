from typing import Type, Union

from src.apps.enums import BlockType
from src.apps.blocks.models import (
    TextBlockModel,
    ImageBlockModel,
    QuestionBlockModel,
    EmailBlockModel,
    CSVBlockModel,
    ExcelBlockModel,
    APIBlockModel,
)
from src.api.v1.blocks.schemas import (
    UnionBlockReadSchema,
    TextBlockReadSchema,
    ImageBlockReadSchema,
    QuestionBlockReadSchema,
    EmailBlockReadSchema,
    CSVBlockReadSchema,
    ExcelBlockReadSchema,
    APIBlockReadSchema,
)

UnionBlockModel = Union[
    TextBlockModel,
    ImageBlockModel,
    QuestionBlockModel,
    EmailBlockModel,
    CSVBlockModel,
    ExcelBlockModel,
    APIBlockModel,
]


def get_block_model_by_type(block_type: BlockType) -> Type[UnionBlockModel]:
    types_to_blocks = {
        BlockType.TEXT_BLOCK.value: TextBlockModel,
        BlockType.IMAGE_BLOCK.value: ImageBlockModel,
        BlockType.QUESTION_BLOCK.value: QuestionBlockModel,
        BlockType.EMAIL_BLOCK.value: EmailBlockModel,
        BlockType.CSV_BLOCK.value: CSVBlockModel,
        BlockType.EXCEL_BLOCK.value: ExcelBlockModel,
        BlockType.API_BLOCK.value: APIBlockModel,
    }
    return types_to_blocks[block_type]


def validate_block_from_db(block: UnionBlockModel) -> UnionBlockReadSchema:
    block_schema = get_block_schema_by_type(block.type)
    return block_schema.model_validate(block)


def get_block_schema_by_type(block_type: BlockType) -> Type[UnionBlockReadSchema]:
    types_to_blocks = {
        BlockType.TEXT_BLOCK.value: TextBlockReadSchema,
        BlockType.IMAGE_BLOCK.value: ImageBlockReadSchema,
        BlockType.QUESTION_BLOCK.value: QuestionBlockReadSchema,
        BlockType.EMAIL_BLOCK.value: EmailBlockReadSchema,
        BlockType.CSV_BLOCK.value: CSVBlockReadSchema,
        BlockType.EXCEL_BLOCK.value: ExcelBlockReadSchema,
        BlockType.API_BLOCK.value: APIBlockReadSchema,
    }
    return types_to_blocks[block_type]


def escape_inner_text(text: str) -> str:
    return text.replace('"', '\\"').replace('\n', '\\n')
