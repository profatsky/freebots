from typing import Annotated

from fastapi import Depends

from src.users.services import UserService

UserServiceDI = Annotated[UserService, Depends(UserService)]
