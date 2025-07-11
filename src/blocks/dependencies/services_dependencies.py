from typing import Annotated

from fastapi import Depends

from src.blocks.services import BlockService

BlockServiceDI = Annotated[BlockService, Depends(BlockService)]
