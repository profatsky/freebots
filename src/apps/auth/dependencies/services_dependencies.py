from typing import Annotated

from fastapi import Depends

from src.apps.auth.services import AuthService

AuthServiceDI = Annotated[AuthService, Depends(AuthService)]
