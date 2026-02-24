from typing import Literal, Self

from pydantic import BaseModel, Field

from src.api.v1.blocks.schemas.base import BlockReadSchema, BlockCreateSchema, BlockUpdateSchema
from src.apps.blocks.dto.question import QuestionBlockCreateDTO, QuestionBlockReadDTO, QuestionBlockUpdateDTO
from src.apps.enums import AnswerMessageType, BlockType


class BaseQuestionBlockSchema(BaseModel):
    message_text: str = Field(max_length=4096)
    answer_type: AnswerMessageType
    type: Literal[BlockType.QUESTION_BLOCK]

    @property
    def is_draft(self) -> bool:
        return not (self.message_text and self.answer_type)


class QuestionBlockReadSchema(BaseQuestionBlockSchema, BlockReadSchema):
    @classmethod
    def from_dto(cls, dto: QuestionBlockReadDTO) -> Self:
        return cls(
            block_id=dto.block_id,
            sequence_number=dto.sequence_number,
            type=dto.type,
            message_text=dto.message_text,
            answer_type=dto.answer_type,
        )


class QuestionBlockCreateSchema(BaseQuestionBlockSchema, BlockCreateSchema):
    def to_dto(self) -> QuestionBlockCreateDTO:
        return QuestionBlockCreateDTO(
            type=self.type,
            message_text=self.message_text,
            answer_type=self.answer_type,
        )


class QuestionBlockUpdateSchema(BaseQuestionBlockSchema, BlockUpdateSchema):
    def to_dto(self) -> QuestionBlockUpdateDTO:
        return QuestionBlockUpdateDTO(
            type=self.type,
            message_text=self.message_text,
            answer_type=self.answer_type,
        )
