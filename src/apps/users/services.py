from uuid import UUID

from src.apps.users.dependencies.repositories_dependencies import UserRepositoryDI
from src.apps.users.dto import UserReadDTO
from src.apps.users.exceptions.services_exceptions import UserAlreadyExistsError, UserNotFoundError


class UserService:
    def __init__(self, user_repository: UserRepositoryDI):
        self._user_repository = user_repository

    async def create_user(self, tg_id: int) -> UserReadDTO:
        user = await self._user_repository.create_user(tg_id)
        if user is None:
            raise UserAlreadyExistsError
        return user

    async def get_user_by_tg_id(self, tg_id: int) -> UserReadDTO:
        user = await self._user_repository.get_user_by_tg_id(tg_id)
        if user is None:
            raise UserNotFoundError
        return user

    async def get_user_by_id(self, user_id: UUID) -> UserReadDTO:
        user = await self._user_repository.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError
        return user

    async def raise_error_if_not_exists(self, user_id: UUID):
        if not await self._user_repository.exists_by_id(user_id):
            raise UserNotFoundError
