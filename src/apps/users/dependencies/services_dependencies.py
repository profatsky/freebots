from typing import Annotated

from fastapi import Depends

from src.apps.users.services import UserService

UserServiceDI = Annotated[UserService, Depends(UserService)]
