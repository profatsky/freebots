from typing import Union, Literal, Annotated

from pydantic import BaseModel, Field, HttpUrl, field_serializer, field_validator

from src.enums import BlockType, AnswerMessageType, HTTPMethod


class BlockReadSchema(BaseModel):
    block_id: int
    sequence_number: int = Field(ge=1)

    model_config = {
        'from_attributes': True,
    }


class BlockCreateSchema(BaseModel):
    pass


class BlockUpdateSchema(BaseModel):
    pass


# Text block
class BaseTextBlockSchema(BaseModel):
    message_text: str = Field(max_length=4096)
    type: Literal[BlockType.TEXT_BLOCK.value]

    @property
    def is_draft(self) -> bool:
        return not bool(self.message_text)


class TextBlockReadSchema(BaseTextBlockSchema, BlockReadSchema):
    pass


class TextBlockCreateSchema(BaseTextBlockSchema, BlockCreateSchema):
    pass


class TextBlockUpdateSchema(BaseTextBlockSchema, BlockUpdateSchema):
    pass


# Image block
class BaseImageBlockSchema(BaseModel):
    image_path: str = Field(max_length=256)
    type: Literal[BlockType.IMAGE_BLOCK.value]

    @property
    def is_draft(self) -> bool:
        return not bool(self.image_path)


class ImageBlockReadSchema(BaseImageBlockSchema, BlockReadSchema):
    pass


class ImageBlockCreateSchema(BaseImageBlockSchema, BlockCreateSchema):
    pass


class ImageBlockUpdateSchema(BaseImageBlockSchema, BlockUpdateSchema):
    pass


# Question block
class BaseQuestionBlockSchema(BaseModel):
    message_text: str = Field(max_length=4096)
    answer_type: AnswerMessageType
    type: Literal[BlockType.QUESTION_BLOCK.value]

    @property
    def is_draft(self) -> bool:
        return not (self.message_text and self.answer_type)


class QuestionBlockReadSchema(BaseQuestionBlockSchema, BlockReadSchema):
    pass


class QuestionBlockCreateSchema(BaseQuestionBlockSchema, BlockCreateSchema):
    pass


class QuestionBlockUpdateSchema(BaseQuestionBlockSchema, BlockUpdateSchema):
    pass


# Email block
class EmailBlockSchema(BaseModel):
    subject: str = Field(max_length=128)
    text: str = Field(max_length=8192)
    recipient_email: str = Field(max_length=254)
    type: Literal[BlockType.EMAIL_BLOCK.value]

    @property
    def is_draft(self) -> bool:
        return not (self.subject and self.text and self.recipient_email)


class EmailBlockReadSchema(EmailBlockSchema, BlockReadSchema):
    pass


class EmailBlockCreateSchema(EmailBlockSchema, BlockCreateSchema):
    pass


class EmailBlockUpdateSchema(EmailBlockSchema, BlockUpdateSchema):
    pass


# CSV block
class CSVBlockSchema(BaseModel):
    file_path: str = Field(max_length=256)
    data: dict[str, Union[int, str]]
    type: Literal[BlockType.CSV_BLOCK.value]

    @field_validator('data')
    @classmethod
    def check_data_length(cls, v: dict[str, Union[int, str]]) -> dict[str, Union[int, str]]:
        if len(v) > 25:
            raise ValueError('The length of the "data" field should not exceed 25')
        return v

    @property
    def is_draft(self) -> bool:
        return not (self.file_path and self.data)


class CSVBlockReadSchema(CSVBlockSchema, BlockReadSchema):
    pass


class CSVBlockCreateSchema(CSVBlockSchema, BlockCreateSchema):
    pass


class CSVBlockUpdateSchema(CSVBlockSchema, BlockUpdateSchema):
    pass


# API block
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
    pass


class APIBlockCreateSchema(APIBlockSchema, BlockCreateSchema):
    @field_serializer('url')
    def serialize_url(self, url: Union[HttpUrl, str]):
        return str(url)


class APIBlockUpdateSchema(APIBlockSchema, BlockUpdateSchema):
    pass


UnionBlockReadSchema = Annotated[
    Union[
        TextBlockReadSchema,
        ImageBlockReadSchema,
        QuestionBlockReadSchema,
        EmailBlockReadSchema,
        CSVBlockReadSchema,
        APIBlockReadSchema,
    ],
    Field(discriminator='type')
]
UnionBlockCreateSchema = Annotated[
    Union[
        TextBlockCreateSchema,
        ImageBlockCreateSchema,
        QuestionBlockCreateSchema,
        EmailBlockCreateSchema,
        CSVBlockCreateSchema,
        APIBlockCreateSchema,
    ],
    Field(discriminator='type')
]

UnionBlockUpdateSchema = Annotated[
    Union[
        TextBlockUpdateSchema,
        ImageBlockUpdateSchema,
        QuestionBlockUpdateSchema,
        EmailBlockUpdateSchema,
        CSVBlockUpdateSchema,
        APIBlockUpdateSchema,
    ],
    Field(discriminator='type')
]
