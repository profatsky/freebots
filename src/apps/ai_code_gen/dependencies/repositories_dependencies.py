from typing import Annotated

from fastapi import Depends

from src.apps.ai_code_gen.repositories import AICodeGenRepository

AICodeGenRepositoryDI = Annotated[AICodeGenRepository, Depends(AICodeGenRepository)]
