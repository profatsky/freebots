from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.apps.projects.models import ProjectModel
from src.apps.users.models import UserModel
from src.infrastructure.db.sessions import Base


class DownloadModel(Base):
    __tablename__ = 'downloads'

    download_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(UserModel.user_id, ondelete='CASCADE'),
        nullable=False,
    )
    project_id: Mapped[UUID] = mapped_column(
        ForeignKey(ProjectModel.project_id, ondelete='SET NULL'),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
