from typing import Annotated

from fastapi import Depends

from src.apps.blocks.services import BlockService

BlockServiceDI = Annotated[BlockService, Depends(BlockService)]
