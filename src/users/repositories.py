from typing import Optional

from passlib.hash import bcrypt
from pydantic import EmailStr
from sqlalchemy import select, func, delete
from sqlalchemy.exc import IntegrityError

from src.auth.schemas import AuthCredentialsSchema, Password
from src.infrastructure.db.dependencies import AsyncSessionDI
from src.projects.models import ProjectModel
from src.users.models import UserModel
from src.users.schemas import UserReadSchema, UserWithStatsReadSchema


class UserRepository:
    def __init__(self, session: AsyncSessionDI):
        self._session = session

    async def create_user(
        self,
        credentials: AuthCredentialsSchema,
    ) -> Optional[UserReadSchema]:
        user = UserModel(email=credentials.email, hashed_password=self._hash_password(credentials.password))
        try:
            self._session.add(user)
            await self._session.commit()
        except IntegrityError:
            return

        return UserReadSchema.model_validate(user)

    @staticmethod
    def _hash_password(password: Password) -> str:
        return bcrypt.hash(password)

    async def get_user_by_email(
        self,
        email: EmailStr,
    ) -> Optional[UserReadSchema]:
        user = await self._get_user_model_instance_by_email(email)
        if user is None:
            return
        return UserReadSchema.model_validate(user)

    async def _get_user_model_instance_by_email(self, email: EmailStr) -> Optional[UserModel]:
        user = await self._session.execute(
            select(UserModel).where(
                UserModel.email == email,
            )
        )
        return user.scalar()

    async def get_user_by_credentials(self, credentials: AuthCredentialsSchema) -> Optional[UserReadSchema]:
        user = await self._get_user_model_instance_by_email(credentials.email)
        if user is None or not self._verify_password(credentials.password, user.hashed_password):
            return
        return UserReadSchema.model_validate(user)

    @staticmethod
    def _verify_password(
        plain_password: Password,
        hashed_password: str,
    ) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> Optional[UserReadSchema]:
        user = await self._get_user_model_instance_by_id(user_id)
        if user is None:
            return
        return UserReadSchema.model_validate(user)

    async def _get_user_model_instance_by_id(self, user_id: int) -> Optional[UserModel]:
        user = await self._session.execute(select(UserModel).where(UserModel.user_id == user_id))
        return user.scalar()

    async def get_user_with_stats(self, user_id: int) -> Optional[UserWithStatsReadSchema]:
        query = (
            self._session.sync_session.query(UserModel, func.count(ProjectModel.project_id).label('project_count'))
            .outerjoin(UserModel.projects)
            .where(UserModel.user_id == user_id)
            .group_by(UserModel.user_id)
        )
        result = (await self._session.execute(query)).first()
        if result is None:
            return
        user, project_count = result

        return UserWithStatsReadSchema(**user.__dict__, project_count=project_count)

    async def delete_user(self, user_id: int):
        await self._session.execute(
            delete(UserModel).where(
                UserModel.user_id == user_id,
            )
        )
        await self._session.commit()
