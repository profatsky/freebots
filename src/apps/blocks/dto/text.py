from dataclasses import dataclass
from typing import Literal

from src.apps.blocks.dto.base import BlockReadDTO, BlockCreateDTO, BlockUpdateDTO
from src.apps.enums import BlockType


@dataclass(frozen=True, kw_only=True)
class BaseTextBlockDTO:
    message_text: str
    type: Literal[BlockType.TEXT_BLOCK] = BlockType.TEXT_BLOCK

    def __post_init__(self):
        self._validate_message_text()

    def _validate_message_text(self):
        if len(self.message_text) > 4096:
            raise ValueError('Invalid message text')


@dataclass(frozen=True)
class TextBlockReadDTO(BaseTextBlockDTO, BlockReadDTO):
    pass


@dataclass(frozen=True)
class TextBlockCreateDTO(BaseTextBlockDTO, BlockCreateDTO):
    pass


@dataclass(frozen=True)
class TextBlockUpdateDTO(BaseTextBlockDTO, BlockUpdateDTO):
    pass
