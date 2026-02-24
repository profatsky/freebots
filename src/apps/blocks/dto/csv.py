from dataclasses import dataclass
from typing import Literal

from src.apps.blocks.dto.base import BlockReadDTO, BlockCreateDTO, BlockUpdateDTO
from src.apps.enums import BlockType


# TODO: Union with Excel
@dataclass(frozen=True, kw_only=True)
class BaseCSVBlockDTO:
    file_path: str
    data: dict[str, int | str]
    type: Literal[BlockType.CSV_BLOCK] = BlockType.CSV_BLOCK

    def __post_init__(self):
        self._validate_file_path()

    def _validate_file_path(self):
        if len(self.file_path) > 256:
            raise ValueError('Invalid file path')

    def _validate_data(self):
        if len(self.data) > 25:
            raise ValueError('Invalid data')

    @property
    def is_draft(self) -> bool:
        return not (self.file_path and self.data)


@dataclass(frozen=True)
class CSVBlockReadDTO(BaseCSVBlockDTO, BlockReadDTO):
    pass


@dataclass(frozen=True)
class CSVBlockCreateDTO(BaseCSVBlockDTO, BlockCreateDTO):
    pass


@dataclass(frozen=True)
class CSVBlockUpdateDTO(BaseCSVBlockDTO, BlockUpdateDTO):
    pass
