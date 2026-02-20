from typing import Optional
from uuid import UUID

from sqlalchemy import select, delete, exists
from sqlalchemy.exc import IntegrityError

from src.apps.users.dto import UserReadDTO
from src.core.base_repository import BaseRepository
from src.apps.users.models import UserModel


class UserRepository(BaseRepository):
    async def create_user(self, tg_id: int, is_superuser: bool = False) -> Optional[UserReadDTO]:
        user = UserModel(tg_id=tg_id, is_superuser=is_superuser)
        try:
            self._session.add(user)
            await self._session.commit()
        except IntegrityError:
            return None

        return user.to_dto()

    async def get_user_by_tg_id(self, tg_id: int) -> Optional[UserReadDTO]:
        user = await self._get_user_model_instance_by_tg_id(tg_id)
        if user is None:
            return None
        return user.to_dto()

    async def _get_user_model_instance_by_tg_id(self, tg_id: int) -> Optional[UserModel]:
        user = await self._session.execute(
            select(UserModel).where(
                UserModel.tg_id == tg_id,
            )
        )
        return user.scalar()

    async def get_user_by_id(self, user_id: UUID) -> Optional[UserReadDTO]:
        user = await self._get_user_model_instance_by_id(user_id)
        if user is None:
            return None
        return user.to_dto()

    async def _get_user_model_instance_by_id(self, user_id: UUID) -> Optional[UserModel]:
        user = await self._session.execute(select(UserModel).where(UserModel.user_id == user_id))
        return user.scalar()

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
