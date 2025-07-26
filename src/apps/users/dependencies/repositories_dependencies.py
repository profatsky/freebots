from typing import Annotated

from fastapi import Depends

from src.apps.users.repositories import UserRepository

UserRepositoryDI = Annotated[UserRepository, Depends(UserRepository)]
