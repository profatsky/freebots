import datetime

from sqlalchemy import String, DateTime, func, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.enums import KeyboardType
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

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))
    user: Mapped['UserModel'] = relationship(back_populates='projects')

    dialogues: Mapped[list['DialogueModel']] = relationship(back_populates='project')

    plugins: Mapped[list['PluginModel']] = relationship(
        secondary=projects_plugins,
        back_populates='projects',
    )
