import datetime

from sqlalchemy import String, Table, Column, Integer, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM

from src.apps.enums import TriggerEventType
from src.apps.plugins.dto import PluginReadDTO, PluginTriggerReadDTO
from src.infrastructure.db.sessions import Base


projects_plugins = Table(
    'projects_plugins',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.project_id', ondelete='CASCADE'), primary_key=True),
    Column('plugin_id', Integer, ForeignKey('plugins.plugin_id', ondelete='CASCADE'), primary_key=True),
)


class PluginModel(Base):
    __tablename__ = 'plugins'

    plugin_id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(128), unique=True)
    summary: Mapped[str] = mapped_column(String(512))
    image_path: Mapped[str] = mapped_column(String(512))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    handlers_file_path: Mapped[str] = mapped_column(String(256))
    db_funcs_file_path: Mapped[str] = mapped_column(String(256))
    readme_file_path: Mapped[str] = mapped_column(String(256))

    triggers: Mapped[list['PluginTriggerModel']] = relationship(back_populates='plugin')
    projects: Mapped[list['ProjectModel']] = relationship(
        secondary=projects_plugins,
        back_populates='plugins',
    )

    def to_dto(self) -> PluginReadDTO:
        triggers = [trigger.to_dto() for trigger in self.triggers]
        return PluginReadDTO(
            plugin_id=self.plugin_id,
            name=self.name,
            summary=self.summary,
            image_path=self.image_path,
            created_at=self.created_at,
            handlers_file_path=self.handlers_file_path,
            db_funcs_file_path=self.db_funcs_file_path,
            readme_file_path=self.readme_file_path,
            triggers=triggers,
        )


class PluginTriggerModel(Base):
    __tablename__ = 'plugin_triggers'

    trigger_id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[TriggerEventType] = mapped_column(ENUM(TriggerEventType, create_type=False), nullable=False)
    value: Mapped[str] = mapped_column(String(64))
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)

    plugin_id: Mapped[int] = mapped_column(ForeignKey('plugins.plugin_id', ondelete='CASCADE'), nullable=False)
    plugin: Mapped[PluginModel] = relationship(back_populates='triggers')

    def to_dto(self) -> PluginTriggerReadDTO:
        return PluginTriggerReadDTO(
            trigger_id=self.trigger_id,
            event_type=self.event_type,
            value=self.value,
            is_admin=self.is_admin,
        )
