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
        BlockType.TEXT_BLOCK.value: TextBlockModel,
        BlockType.IMAGE_BLOCK.value: ImageBlockModel,
        BlockType.QUESTION_BLOCK.value: QuestionBlockModel,
        BlockType.EMAIL_BLOCK.value: EmailBlockModel,
        BlockType.CSV_BLOCK.value: CSVBlockModel,
        BlockType.EXCEL_BLOCK.value: ExcelBlockModel,
        BlockType.API_BLOCK.value: APIBlockModel,
    }
    return types_to_blocks[block_type]  # TODO: fix type hint


def escape_inner_text(text: str) -> str:
    return text.replace('"', '\\"').replace('\n', '\\n')
