from sqlalchemy import String, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.blocks.dto.api import APIBlockReadDTO
from src.apps.blocks.dto.base import BlockReadDTO
from src.apps.blocks.dto.csv import CSVBlockReadDTO
from src.apps.blocks.dto.email import EmailBlockReadDTO
from src.apps.blocks.dto.excel import ExcelBlockReadDTO
from src.apps.blocks.dto.image import ImageBlockReadDTO
from src.apps.blocks.dto.question import QuestionBlockReadDTO
from src.apps.blocks.dto.text import TextBlockReadDTO
from src.infrastructure.db.sessions import Base
from src.apps.enums import AnswerMessageType, HTTPMethod
from src.apps.dialogues.models import DialogueModel


class BlockModel(Base):
    __tablename__ = 'blocks'

    block_id: Mapped[int] = mapped_column(primary_key=True)

    dialogue_id: Mapped[int] = mapped_column(ForeignKey('dialogues.dialogue_id', ondelete='CASCADE'))
    dialogue: Mapped[DialogueModel] = relationship(back_populates='blocks')

    sequence_number: Mapped[int]

    type: Mapped[str]

    __mapper_args__ = {
        'polymorphic_identity': 'blocks',
        'polymorphic_on': 'type',
    }

    __table_args__ = (UniqueConstraint('dialogue_id', 'sequence_number'),)

    def to_dto(self) -> BlockReadDTO:
        raise NotImplementedError


class TextBlockModel(BlockModel):
    __tablename__ = 'text_blocks'

    block_id: Mapped[int] = mapped_column(ForeignKey('blocks.block_id', ondelete='CASCADE'), primary_key=True)

    message_text: Mapped[str] = mapped_column(String(4096))

    __mapper_args__ = {
        'polymorphic_identity': 'text_block',
    }

    def to_dto(self) -> TextBlockReadDTO:
        return TextBlockReadDTO(
            block_id=self.block_id,
            sequence_number=self.sequence_number,
            type=self.type,  # TODO: fix type hint
            message_text=self.message_text,
        )


class ImageBlockModel(BlockModel):
    __tablename__ = 'image_blocks'

    block_id: Mapped[int] = mapped_column(ForeignKey('blocks.block_id', ondelete='CASCADE'), primary_key=True)

    image_path: Mapped[str] = mapped_column(String(4096))

    __mapper_args__ = {
        'polymorphic_identity': 'image_block',
    }

    def to_dto(self) -> ImageBlockReadDTO:
        return ImageBlockReadDTO(
            block_id=self.block_id,
            sequence_number=self.sequence_number,
            type=self.type,  # TODO: fix type hint
            image_path=self.image_path,
        )


class QuestionBlockModel(BlockModel):
    __tablename__ = 'question_blocks'

    block_id: Mapped[int] = mapped_column(ForeignKey('blocks.block_id', ondelete='CASCADE'), primary_key=True)

    message_text: Mapped[str] = mapped_column(String(4096))
    answer_type: Mapped[AnswerMessageType] = mapped_column(Enum(AnswerMessageType).values_callable, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'question_block',
    }

    def to_dto(self) -> QuestionBlockReadDTO:
        return QuestionBlockReadDTO(
            block_id=self.block_id,
            sequence_number=self.sequence_number,
            type=self.type,  # TODO: fix type hint
            message_text=self.message_text,
            answer_type=self.answer_type,
        )


class EmailBlockModel(BlockModel):
    __tablename__ = 'email_blocks'

    block_id: Mapped[int] = mapped_column(ForeignKey('blocks.block_id', ondelete='CASCADE'), primary_key=True)

    subject: Mapped[str] = mapped_column(String(128))
    text: Mapped[str] = mapped_column(String(8192))
    recipient_email: Mapped[str] = mapped_column(String(254))

    __mapper_args__ = {
        'polymorphic_identity': 'email_block',
    }

    def to_dto(self) -> EmailBlockReadDTO:
        return EmailBlockReadDTO(
            block_id=self.block_id,
            sequence_number=self.sequence_number,
            type=self.type,  # TODO: fix type hint
            subject=self.subject,
            text=self.text,
            recipient_email=self.recipient_email,
        )


class CSVBlockModel(BlockModel):
    __tablename__ = 'csv_blocks'

    block_id: Mapped[int] = mapped_column(ForeignKey('blocks.block_id', ondelete='CASCADE'), primary_key=True)

    file_path: Mapped[str] = mapped_column(String(256))
    data: Mapped[dict] = mapped_column(JSONB)

    __mapper_args__ = {
        'polymorphic_identity': 'csv_block',
    }

    def to_dto(self) -> CSVBlockReadDTO:
        return CSVBlockReadDTO(
            block_id=self.block_id,
            sequence_number=self.sequence_number,
            type=self.type,  # TODO: fix type hint
            file_path=self.file_path,
            data=self.data,
        )


class ExcelBlockModel(BlockModel):
    __tablename__ = 'excel_blocks'

    block_id: Mapped[int] = mapped_column(ForeignKey('blocks.block_id', ondelete='CASCADE'), primary_key=True)

    file_path: Mapped[str] = mapped_column(String(256))
    data: Mapped[dict] = mapped_column(JSONB)

    __mapper_args__ = {
        'polymorphic_identity': 'excel_block',
    }

    def to_dto(self) -> ExcelBlockReadDTO:
        return ExcelBlockReadDTO(
            block_id=self.block_id,
            sequence_number=self.sequence_number,
            type=self.type,  # TODO: fix type hint
            file_path=self.file_path,
            data=self.data,
        )


class APIBlockModel(BlockModel):
    __tablename__ = 'api_blocks'

    block_id: Mapped[int] = mapped_column(ForeignKey('blocks.block_id', ondelete='CASCADE'), primary_key=True)

    url: Mapped[str] = mapped_column(String(2048))
    http_method: Mapped[HTTPMethod] = mapped_column(Enum(HTTPMethod).values_callable, nullable=False)
    headers: Mapped[dict] = mapped_column(JSONB)
    body: Mapped[dict] = mapped_column(JSONB)

    __mapper_args__ = {
        'polymorphic_identity': 'api_block',
    }

    def to_dto(self) -> APIBlockReadDTO:
        return APIBlockReadDTO(
            block_id=self.block_id,
            sequence_number=self.sequence_number,
            type=self.type,  # TODO: fix type hint
            url=self.url,
            http_method=self.http_method,
            headers=self.headers,
            body=self.body,
        )
