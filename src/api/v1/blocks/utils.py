from src.api.v1.blocks.schemas import (
    TextBlockReadSchema,
    ImageBlockReadSchema,
    QuestionBlockReadSchema,
    EmailBlockReadSchema,
    CSVBlockReadSchema,
    ExcelBlockReadSchema,
    APIBlockReadSchema,
)
from src.api.v1.blocks.schemas.base import BlockReadSchema
from src.apps.blocks.dto.base import BlockReadDTO
from src.apps.enums import BlockType


def _get_block_read_schema_by_type(block_type: BlockType) -> type[BlockReadSchema]:
    type_to_schema = {
        BlockType.TEXT_BLOCK: TextBlockReadSchema,
        BlockType.IMAGE_BLOCK: ImageBlockReadSchema,
        BlockType.QUESTION_BLOCK: QuestionBlockReadSchema,
        BlockType.EMAIL_BLOCK: EmailBlockReadSchema,
        BlockType.CSV_BLOCK: CSVBlockReadSchema,
        BlockType.EXCEL_BLOCK: ExcelBlockReadSchema,
        BlockType.API_BLOCK: APIBlockReadSchema,
    }
    return type_to_schema[block_type]


def convert_block_read_dto_to_schema(dto: BlockReadDTO) -> BlockReadSchema:
    schema_cls = _get_block_read_schema_by_type(dto.type)
    return schema_cls.from_dto(dto)
