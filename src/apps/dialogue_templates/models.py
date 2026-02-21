import datetime

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.dialogue_templates.dto import DialogueTemplateReadDTO
from src.infrastructure.db.sessions import Base


class DialogueTemplateModel(Base):
    __tablename__ = 'templates'

    template_id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(128), unique=True)
    summary: Mapped[str] = mapped_column(String(512))
    description: Mapped[str] = mapped_column(String(4096))
    image_path: Mapped[str] = mapped_column(String(512))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    readme_file_path: Mapped[str] = mapped_column(String(256))

    dialogue_id: Mapped[int] = mapped_column(ForeignKey('dialogues.dialogue_id', ondelete='CASCADE'))
    dialogue: Mapped['DialogueModel'] = relationship(back_populates='template')

    def to_dto(self) -> DialogueTemplateReadDTO:
        return DialogueTemplateReadDTO(
            template_id=self.template_id,
            name=self.name,
            summary=self.summary,
            description=self.description,
            image_path=self.image_path,
            created_at=self.created_at,
            readme_file_path=self.readme_file_path,
        )
