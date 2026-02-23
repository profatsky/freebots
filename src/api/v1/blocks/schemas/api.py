from typing import Union, Literal, Self

from pydantic import BaseModel, HttpUrl, field_validator, field_serializer

from src.api.v1.blocks.schemas.base import BlockReadSchema, BlockCreateSchema, BlockUpdateSchema
from src.apps.blocks.dto.api import APIBlockReadDTO, APIBlockCreateDTO, APIBlockUpdateDTO
from src.apps.enums import HTTPMethod, BlockType


# TODO url validation
class APIBlockSchema(BaseModel):
    url: Union[HttpUrl, str]
    http_method: HTTPMethod
    headers: dict[str, str]
    body: dict[str, Union[str, int]]
    type: Literal[BlockType.API_BLOCK.value]

    @field_validator('headers')
    @classmethod
    def check_headers_length(cls, v: dict[str, str]) -> dict[str, str]:
        if len(v) > 25:
            raise ValueError('The length of the "headers" field should not exceed 25')
        return v

    @field_validator('body')
    @classmethod
    def check_body_length(cls, v: dict[str, Union[str, int]]) -> dict[str, Union[str, int]]:
        if len(v) > 25:
            raise ValueError('The length of the "body" field should not exceed 25')
        return v

    @property
    def is_draft(self) -> bool:
        return not (self.url and self.http_method)


class APIBlockReadSchema(APIBlockSchema, BlockReadSchema):
    @classmethod
    def from_dto(cls, dto: APIBlockReadDTO) -> Self:
        return cls(
            block_id=dto.block_id,
            sequence_number=dto.sequence_number,
            type=dto.type,
            url=dto.url,
            http_method=dto.http_method,
            headers=dto.headers,
            body=dto.body,
        )


class APIBlockCreateSchema(APIBlockSchema, BlockCreateSchema):
    @field_serializer('url')
    def serialize_url(self, url: Union[HttpUrl, str]):
        return str(url)

    def to_dto(self) -> APIBlockCreateDTO:
        return APIBlockCreateDTO(
            type=self.type,
            url=self.url,
            http_method=self.http_method,
            headers=self.headers,
            body=self.body,
        )


class APIBlockUpdateSchema(APIBlockSchema, BlockUpdateSchema):
    def to_dto(self) -> APIBlockUpdateDTO:
        return APIBlockUpdateDTO(
            type=self.type,
            url=self.url,
            http_method=self.http_method,
            headers=self.headers,
            body=self.body,
        )
