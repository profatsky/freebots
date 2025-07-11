from typing import Annotated

from fastapi import Depends

from src.blocks.repositories import BlockRepository

BlockRepositoryDI = Annotated[BlockRepository, Depends(BlockRepository)]
