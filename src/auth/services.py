from src.auth.dependencies.auth_dependencies import AuthSecurityDI
from src.auth.schemas import AuthCredentialsSchema
from src.users.dependencies.services_dependencies import UserServiceDI


class AuthService:
    def __init__(
        self,
        auth_security: AuthSecurityDI,
        user_service: UserServiceDI,
    ):
        self._auth_security = auth_security
        self._user_service = user_service

    async def register(self, credentials: AuthCredentialsSchema) -> str:
        user = await self._user_service.create_user(credentials)
        return self._create_access_token(user.user_id)

    async def login(self, credentials: AuthCredentialsSchema) -> str:
        user = await self._user_service.get_user_by_credentials(credentials)
        return self._create_access_token(user.user_id)

    def _create_access_token(self, user_id: int) -> str:
        return self._auth_security.create_access_token(uid=str(user_id))
