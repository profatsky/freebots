from typing import Annotated

from fastapi import Depends

from src.apps.blocks.repositories import BlockRepository

BlockRepositoryDI = Annotated[BlockRepository, Depends(BlockRepository)]
