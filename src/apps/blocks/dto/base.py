from dataclasses import dataclass
from typing import Literal, Optional

from src.apps.enums import BlockType


BlockTypeLiteral = Literal[*[t.value for t in BlockType]]


@dataclass(frozen=True)
class BlockReadDTO:
    block_id: int
    sequence_number: int
    type: Optional[BlockTypeLiteral] = None

    def __post_init__(self):
        self._validate_sequence_number()

    def _validate_sequence_number(self):
        if self.sequence_number <= 0:
            raise ValueError('Invalid sequence number')

    @property
    def is_draft(self) -> bool:
        raise NotImplementedError


@dataclass(frozen=True)
class BlockCreateDTO:
    type: Optional[BlockTypeLiteral] = None


@dataclass(frozen=True)
class BlockUpdateDTO:
    pass
