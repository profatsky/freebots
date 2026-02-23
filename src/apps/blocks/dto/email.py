from dataclasses import dataclass
from typing import Literal

from src.apps.blocks.dto.base import BlockReadDTO, BlockCreateDTO, BlockUpdateDTO
from src.apps.enums import BlockType


@dataclass(frozen=True, kw_only=True)
class BaseEmailBlockDTO:
    subject: str
    text: str
    recipient_email: str
    type: Literal[BlockType.QUESTION_BLOCK.value] = BlockType.QUESTION_BLOCK.value

    def __post_init__(self):
        self._validate_subject()
        self._validate_text()
        self._validate_recipient_email()

    def _validate_subject(self):
        if len(self.subject) > 128:
            raise ValueError('Invalid subject')

    def _validate_text(self):
        if len(self.text) > 8192:
            raise ValueError('Invalid text')

    def _validate_recipient_email(self):
        if len(self.recipient_email) > 256:
            raise ValueError('Invalid recipient email')

    @property
    def is_draft(self) -> bool:
        return not (self.subject and self.text and self.recipient_email)


@dataclass(frozen=True)
class EmailBlockReadDTO(BaseEmailBlockDTO, BlockReadDTO):
    pass


@dataclass(frozen=True)
class EmailBlockCreateDTO(BaseEmailBlockDTO, BlockCreateDTO):
    pass


@dataclass(frozen=True)
class EmailBlockUpdateDTO(BaseEmailBlockDTO, BlockUpdateDTO):
    pass
