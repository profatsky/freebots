from typing import Annotated

from fastapi import Depends

from src.apps.code_gen.services import CodeGenService

CodeGenServiceDI = Annotated[CodeGenService, Depends(CodeGenService)]
