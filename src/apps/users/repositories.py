from typing import Optional
from uuid import UUID

from sqlalchemy import select, func, delete, exists
from sqlalchemy.exc import IntegrityError

from src.core.base_repository import BaseRepository
from src.apps.projects.models import ProjectModel
from src.apps.users.models import UserModel
from src.apps.users.schemas import UserReadSchema, UserWithStatsReadSchema


class UserRepository(BaseRepository):
    async def create_user(self, tg_id: int, is_superuser: bool = False) -> Optional[UserReadSchema]:
        user = UserModel(tg_id=tg_id, is_superuser=is_superuser)
        try:
            self._session.add(user)
            await self._session.commit()
        except IntegrityError:
            return None

        return UserReadSchema.model_validate(user)

    async def get_user_by_tg_id(self, tg_id: int) -> Optional[UserReadSchema]:
        user = await self._get_user_model_instance_by_tg_id(tg_id)
        if user is None:
            return None
        return UserReadSchema.model_validate(user)

    async def _get_user_model_instance_by_tg_id(self, tg_id: int) -> Optional[UserModel]:
        user = await self._session.execute(
            select(UserModel).where(
                UserModel.tg_id == tg_id,
            )
        )
        return user.scalar()

    async def get_user_by_id(self, user_id: UUID) -> Optional[UserReadSchema]:
        user = await self._get_user_model_instance_by_id(user_id)
        if user is None:
            return None
        return UserReadSchema.model_validate(user)

    async def _get_user_model_instance_by_id(self, user_id: UUID) -> Optional[UserModel]:
        user = await self._session.execute(select(UserModel).where(UserModel.user_id == user_id))
        return user.scalar()

    async def get_user_with_stats(self, user_id: UUID) -> Optional[UserWithStatsReadSchema]:
        query = (
            self._session.sync_session.query(UserModel, func.count(ProjectModel.project_id).label('project_count'))
            .outerjoin(UserModel.projects)
            .where(UserModel.user_id == user_id)
            .group_by(UserModel.user_id)
        )
        result = (await self._session.execute(query)).first()
        if result is None:
            return None
        user, project_count = result

        return UserWithStatsReadSchema(**user.__dict__, project_count=project_count)

    async def delete_user(self, user_id: UUID):
        await self._session.execute(
            delete(UserModel).where(
                UserModel.user_id == user_id,
            )
        )
        await self._session.commit()

    async def exists_by_id(self, user_id: UUID) -> bool:
        return await self._session.scalar(
            select(
                exists().where(
                    UserModel.user_id == user_id,
                )
            )
        )
