from typing import Annotated

from fastapi import Depends

from src.users.repositories import UserRepository

UserRepositoryDI = Annotated[UserRepository, Depends(UserRepository)]
