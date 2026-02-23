from typing import Type

from src.apps.enums import BlockType
from src.apps.blocks.models import (
    TextBlockModel,
    ImageBlockModel,
    QuestionBlockModel,
    EmailBlockModel,
    CSVBlockModel,
    ExcelBlockModel,
    APIBlockModel,
    BlockModel,
)


def get_block_model_by_type(block_type: BlockType) -> Type[BlockModel]:
    types_to_blocks = {
        BlockType.TEXT_BLOCK: TextBlockModel,
        BlockType.IMAGE_BLOCK: ImageBlockModel,
        BlockType.QUESTION_BLOCK: QuestionBlockModel,
        BlockType.EMAIL_BLOCK: EmailBlockModel,
        BlockType.CSV_BLOCK: CSVBlockModel,
        BlockType.EXCEL_BLOCK: ExcelBlockModel,
        BlockType.API_BLOCK: APIBlockModel,
    }
    return types_to_blocks[block_type]


def escape_inner_text(text: str) -> str:
    return text.replace('"', '\\"').replace('\n', '\\n')
