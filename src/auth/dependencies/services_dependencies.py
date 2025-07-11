from typing import Annotated

from fastapi import Depends

from src.auth.services import AuthService

AuthServiceDI = Annotated[AuthService, Depends(AuthService)]
