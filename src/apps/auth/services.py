from src.apps.auth.dependencies.auth_dependencies import AuthSecurityDI
from src.apps.users.dependencies.repositories_dependencies import UserRepositoryDI
from src.infrastructure.cache.dependencies import CacheClientDI


class AuthService:
    CODE_TTL = 300

    def __init__(
        self,
        auth_security: AuthSecurityDI,
        user_repository: UserRepositoryDI,
        cache_client: CacheClientDI,
    ):
        self._auth_security = auth_security
        self._user_repository = user_repository
        self._cache_cli = cache_client

    async def register_or_login(self, tg_id: int, is_superuser: bool = False):
        user = await self._user_repository.get_user_by_tg_id(tg_id)
        if user is None:
            user = await self._user_repository.create_user(tg_id, is_superuser)
        return self._auth_security.create_access_token(uid=str(user.user_id))

    async def save_tg_code(self, tg_id: int, code: str) -> None:
        key = f'tg_code:{code}'
        await self._cache_cli.set(name=key, value=tg_id, ex=self.CODE_TTL)
