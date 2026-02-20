import datetime
from typing import Self
from uuid import UUID

from sqlalchemy import String, DateTime, func, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.enums import KeyboardType
from src.apps.projects.dto import ProjectCreateDTO, ProjectReadDTO, ProjectWithDialoguesAndPluginsReadDTO
from src.infrastructure.db.sessions import Base
from src.apps.plugins.models import projects_plugins


class ProjectModel(Base):
    __tablename__ = 'projects'

    project_id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(256))
    start_message: Mapped[str] = mapped_column(String(4096))
    start_keyboard_type: Mapped[KeyboardType] = mapped_column(Enum(KeyboardType).values_callable, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))
    user: Mapped['UserModel'] = relationship(back_populates='projects')

    dialogues: Mapped[list['DialogueModel']] = relationship(back_populates='project')

    plugins: Mapped[list['PluginModel']] = relationship(
        secondary=projects_plugins,
        back_populates='projects',
    )

    @classmethod
    def from_dto(cls, project: ProjectCreateDTO) -> Self:
        return ProjectModel(
            user_id=project.user_id,
            name=project.name,
            start_message=project.start_message,
            start_keyboard_type=project.start_keyboard_type,
        )

    def to_dto(self) -> ProjectReadDTO:
        return ProjectReadDTO(
            project_id=self.project_id,
            user_id=self.user_id,
            name=self.name,
            start_message=self.start_message,
            start_keyboard_type=self.start_keyboard_type,
            created_at=self.created_at,
        )

    def to_extended_dto(self) -> ProjectWithDialoguesAndPluginsReadDTO:
        return ProjectWithDialoguesAndPluginsReadDTO(
            project_id=self.project_id,
            user_id=self.user_id,
            name=self.name,
            start_message=self.start_message,
            start_keyboard_type=self.start_keyboard_type,
            created_at=self.created_at,
            dialogues=self.dialogues,
            plugins=self.plugins,
        )
