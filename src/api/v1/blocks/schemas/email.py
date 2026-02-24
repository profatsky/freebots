from typing import Literal, Self

from pydantic import BaseModel, Field

from src.api.v1.blocks.schemas.base import BlockReadSchema, BlockCreateSchema, BlockUpdateSchema
from src.apps.blocks.dto.email import EmailBlockCreateDTO, EmailBlockReadDTO, EmailBlockUpdateDTO
from src.apps.enums import BlockType


class EmailBlockSchema(BaseModel):
    subject: str = Field(max_length=128)
    text: str = Field(max_length=8192)
    recipient_email: str = Field(max_length=256)
    type: Literal[BlockType.EMAIL_BLOCK]

    @property
    def is_draft(self) -> bool:
        return not (self.subject and self.text and self.recipient_email)


class EmailBlockReadSchema(EmailBlockSchema, BlockReadSchema):
    @classmethod
    def from_dto(cls, dto: EmailBlockReadDTO) -> Self:
        return cls(
            block_id=dto.block_id,
            sequence_number=dto.sequence_number,
            type=dto.type,
            subject=dto.subject,
            text=dto.text,
            recipient_email=dto.recipient_email,
        )


class EmailBlockCreateSchema(EmailBlockSchema, BlockCreateSchema):
    def to_dto(self) -> EmailBlockCreateDTO:
        return EmailBlockCreateDTO(
            type=self.type,
            subject=self.subject,
            text=self.text,
            recipient_email=self.recipient_email,
        )


class EmailBlockUpdateSchema(EmailBlockSchema, BlockUpdateSchema):
    def to_dto(self) -> EmailBlockUpdateDTO:
        return EmailBlockUpdateDTO(
            type=self.type,
            subject=self.subject,
            text=self.text,
            recipient_email=self.recipient_email,
        )
