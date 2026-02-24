from dataclasses import dataclass
from typing import Literal

from src.apps.blocks.dto.base import BlockReadDTO, BlockCreateDTO, BlockUpdateDTO
from src.apps.enums import BlockType


@dataclass(frozen=True, kw_only=True)
class BaseImageBlockDTO:
    image_path: str
    type: Literal[BlockType.IMAGE_BLOCK] = BlockType.IMAGE_BLOCK

    @property
    def is_draft(self) -> bool:
        return not bool(self.image_path)


@dataclass(frozen=True)
class ImageBlockReadDTO(BaseImageBlockDTO, BlockReadDTO):
    pass


@dataclass(frozen=True)
class ImageBlockCreateDTO(BaseImageBlockDTO, BlockCreateDTO):
    pass


@dataclass(frozen=True)
class ImageBlockUpdateDTO(BaseImageBlockDTO, BlockUpdateDTO):
    pass
