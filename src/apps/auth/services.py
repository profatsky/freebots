from src.apps.auth.dependencies.auth_dependencies import AuthSecurityDI
from src.apps.users.dependencies.repositories_dependencies import UserRepositoryDI


class AuthService:
    def __init__(
        self,
        auth_security: AuthSecurityDI,
        user_repository: UserRepositoryDI,
    ):
        self._auth_security = auth_security
        self._user_repository = user_repository

    async def register_or_login(self, tg_id: int):
        user = await self._user_repository.get_user_by_tg_id(tg_id)
        if user is None:
            user = await self._user_repository.create_user(tg_id)
        return self._auth_security.create_access_token(uid=str(user.user_id))
