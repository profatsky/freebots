from dataclasses import dataclass
from typing import Literal

from src.apps.blocks.dto.base import BlockReadDTO, BlockCreateDTO, BlockUpdateDTO
from src.apps.enums import BlockType, HTTPMethod


@dataclass(frozen=True, kw_only=True)
class BaseAPIBlockDTO:
    url: str  # TODO: add validation
    http_method: HTTPMethod
    headers: dict[str, str]
    body: dict[str, str | int]
    type: Literal[BlockType.API_BLOCK] = BlockType.API_BLOCK

    def __post_init__(self):
        self._validate_headers()
        self._validate_body()

    def _validate_headers(self):
        if len(self.headers) > 25:
            raise ValueError('Invalid headers')

    def _validate_body(self):
        if len(self.body) > 25:
            raise ValueError('Invalid body')

    @property
    def is_draft(self) -> bool:
        return not (self.url and self.http_method)


@dataclass(frozen=True)
class APIBlockReadDTO(BaseAPIBlockDTO, BlockReadDTO):
    pass


@dataclass(frozen=True)
class APIBlockCreateDTO(BaseAPIBlockDTO, BlockCreateDTO):
    pass


@dataclass(frozen=True)
class APIBlockUpdateDTO(BaseAPIBlockDTO, BlockUpdateDTO):
    pass
