from dataclasses import dataclass
from typing import Literal

from src.apps.blocks.dto.base import BlockReadDTO, BlockCreateDTO, BlockUpdateDTO
from src.apps.enums import BlockType, AnswerMessageType


@dataclass(frozen=True, kw_only=True)
class BaseQuestionBlockDTO:
    message_text: str
    answer_type: AnswerMessageType
    type: Literal[BlockType.QUESTION_BLOCK] = BlockType.QUESTION_BLOCK

    def __post_init__(self):
        self._validate_message_text()

    def _validate_message_text(self):
        if len(self.message_text) > 4096:
            raise ValueError('Invalid message text')

    @property
    def is_draft(self) -> bool:
        return not (self.message_text and self.answer_type)


@dataclass(frozen=True)
class QuestionBlockReadDTO(BaseQuestionBlockDTO, BlockReadDTO):
    pass


@dataclass(frozen=True)
class QuestionBlockCreateDTO(BaseQuestionBlockDTO, BlockCreateDTO):
    pass


@dataclass(frozen=True)
class QuestionBlockUpdateDTO(BaseQuestionBlockDTO, BlockUpdateDTO):
    pass
