import datetime

from sqlalchemy import String, Table, Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


projects_plugins = Table(
    'projects_plugins',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.project_id', ondelete='CASCADE'), primary_key=True),
    Column('plugin_id', Integer, ForeignKey('plugins.plugin_id', ondelete='CASCADE'), primary_key=True)
)


class PluginModel(Base):
    __tablename__ = 'plugins'

    plugin_id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(128), unique=True)
    summary: Mapped[str] = mapped_column(String(512))
    description: Mapped[str] = mapped_column(String(4096))
    image_path: Mapped[str] = mapped_column(String(512))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    handlers_file_path: Mapped[str] = mapped_column(String(256))
    db_funcs_file_path: Mapped[str] = mapped_column(String(256))

    projects: Mapped[list['ProjectModel']] = relationship(
        secondary=projects_plugins,
        back_populates='plugins',
    )
