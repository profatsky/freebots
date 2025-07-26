from pydantic import EmailStr

from src.apps.auth.schemas import AuthCredentialsSchema
from src.apps.users.dependencies.repositories_dependencies import UserRepositoryDI
from src.apps.users.exceptions.services_exceptions import UserAlreadyExistsError, UserNotFoundError
from src.apps.auth.exceptions.services_exceptions import InvalidCredentialsError
from src.apps.users.schemas import UserReadSchema, UserWithStatsReadSchema


class UserService:
    def __init__(self, user_repository: UserRepositoryDI):
        self._user_repository = user_repository

    async def create_user(
        self,
        credentials: AuthCredentialsSchema,
    ) -> UserReadSchema:
        user = await self._user_repository.create_user(credentials)
        if user is None:
            raise UserAlreadyExistsError
        return user

    async def get_user_by_email(
        self,
        email: EmailStr,
    ) -> UserReadSchema:
        user = await self._user_repository.get_user_by_email(email)
        if user is None:
            raise UserNotFoundError
        return user

    async def get_user_by_credentials(
        self,
        credentials: AuthCredentialsSchema,
    ) -> UserReadSchema:
        user = await self._user_repository.get_user_by_credentials(credentials)
        if user is None:
            raise InvalidCredentialsError
        return user

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> UserReadSchema:
        user = await self._user_repository.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError
        return user

    async def get_user_with_stats(
        self,
        user_id: int,
    ) -> UserWithStatsReadSchema:
        user = await self._user_repository.get_user_with_stats(user_id)
        if user is None:
            raise UserNotFoundError
        return user
