from typing import Union, Annotated

from pydantic import Field

from src.api.v1.blocks.schemas.api import APIBlockReadSchema, APIBlockCreateSchema, APIBlockUpdateSchema
from src.api.v1.blocks.schemas.csv import CSVBlockReadSchema, CSVBlockCreateSchema, CSVBlockUpdateSchema
from src.api.v1.blocks.schemas.email import EmailBlockReadSchema, EmailBlockCreateSchema, EmailBlockUpdateSchema
from src.api.v1.blocks.schemas.excel import ExcelBlockReadSchema, ExcelBlockCreateSchema, ExcelBlockUpdateSchema
from src.api.v1.blocks.schemas.image import ImageBlockReadSchema, ImageBlockCreateSchema, ImageBlockUpdateSchema
from src.api.v1.blocks.schemas.question import (
    QuestionBlockReadSchema,
    QuestionBlockCreateSchema,
    QuestionBlockUpdateSchema,
)
from src.api.v1.blocks.schemas.text import TextBlockReadSchema, TextBlockCreateSchema, TextBlockUpdateSchema


UnionBlockReadSchema = Annotated[
    Union[
        TextBlockReadSchema,
        ImageBlockReadSchema,
        QuestionBlockReadSchema,
        EmailBlockReadSchema,
        CSVBlockReadSchema,
        ExcelBlockReadSchema,
        APIBlockReadSchema,
    ],
    Field(discriminator='type'),
]

UnionBlockCreateSchema = Annotated[
    Union[
        TextBlockCreateSchema,
        ImageBlockCreateSchema,
        QuestionBlockCreateSchema,
        EmailBlockCreateSchema,
        CSVBlockCreateSchema,
        ExcelBlockCreateSchema,
        APIBlockCreateSchema,
    ],
    Field(discriminator='type'),
]

UnionBlockUpdateSchema = Annotated[
    Union[
        TextBlockUpdateSchema,
        ImageBlockUpdateSchema,
        QuestionBlockUpdateSchema,
        EmailBlockUpdateSchema,
        CSVBlockUpdateSchema,
        ExcelBlockUpdateSchema,
        APIBlockUpdateSchema,
    ],
    Field(discriminator='type'),
]
