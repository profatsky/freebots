from typing import Annotated

from fastapi import Depends

from src.apps.ai_code_gen.services import AICodeGenService

AICodeGenServiceDI = Annotated[AICodeGenService, Depends(AICodeGenService)]
