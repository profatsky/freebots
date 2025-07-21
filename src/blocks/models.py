from sqlalchemy import String, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base
from src.enums import AnswerMessageType, HTTPMethod
from src.dialogues.models import DialogueModel


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


class TextBlockModel(BlockModel):
    __tablename__ = 'text_blocks'

    block_id: Mapped[int] = mapped_column(ForeignKey('blocks.block_id', ondelete='CASCADE'), primary_key=True)

    message_text: Mapped[str] = mapped_column(String(4096))

    __mapper_args__ = {
        'polymorphic_identity': 'text_block',
    }


class ImageBlockModel(BlockModel):
    __tablename__ = 'image_blocks'

    block_id: Mapped[int] = mapped_column(ForeignKey('blocks.block_id', ondelete='CASCADE'), primary_key=True)

    image_path: Mapped[str] = mapped_column(String(4096))

    __mapper_args__ = {
        'polymorphic_identity': 'image_block',
    }


class QuestionBlockModel(BlockModel):
    __tablename__ = 'question_blocks'

    block_id: Mapped[int] = mapped_column(ForeignKey('blocks.block_id', ondelete='CASCADE'), primary_key=True)

    message_text: Mapped[str] = mapped_column(String(4096))
    answer_type: Mapped[AnswerMessageType] = mapped_column(Enum(AnswerMessageType).values_callable, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'question_block',
    }


class EmailBlockModel(BlockModel):
    __tablename__ = 'email_blocks'

    block_id: Mapped[int] = mapped_column(ForeignKey('blocks.block_id', ondelete='CASCADE'), primary_key=True)

    subject: Mapped[str] = mapped_column(String(128))
    text: Mapped[str] = mapped_column(String(8192))
    recipient_email: Mapped[str] = mapped_column(String(254))

    __mapper_args__ = {
        'polymorphic_identity': 'email_block',
    }


class CSVBlockModel(BlockModel):
    __tablename__ = 'csv_blocks'

    block_id: Mapped[int] = mapped_column(ForeignKey('blocks.block_id', ondelete='CASCADE'), primary_key=True)

    file_path: Mapped[str] = mapped_column(String(256))
    data: Mapped[dict] = mapped_column(JSONB)

    __mapper_args__ = {
        'polymorphic_identity': 'csv_block',
    }


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
