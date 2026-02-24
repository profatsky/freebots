from typing import Annotated

from fastapi import Depends

from src.apps.code_gen.repositories import CodeGenRepository

CodeGenRepositoryDI = Annotated[CodeGenRepository, Depends(CodeGenRepository)]
