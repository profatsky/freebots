from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.orm import selectin_polymorphic

from src.apps.blocks.dto.base import BlockCreateDTO, BlockReadDTO, BlockUpdateDTO
from src.apps.blocks.models import BlockModel
from src.apps.blocks import utils
from src.core.base_repository import BaseRepository


class BlockRepository(BaseRepository):
    async def create_block(
        self,
        dialogue_id: int,
        block: BlockCreateDTO,
    ) -> BlockReadDTO:
        blocks = await self.get_blocks(dialogue_id)

        block_model = utils.get_block_model_by_type(block.type)
        block = block_model(**block.__dict__, dialogue_id=dialogue_id, sequence_number=len(blocks) + 1)
        self._session.add(block)
        await self._session.commit()

        return block.to_dto()

    async def get_blocks(self, dialogue_id: int) -> list[BlockReadDTO]:
        blocks = await self._get_blocks(dialogue_id)
        return [block.to_dto() for block in blocks]

    async def _get_blocks(self, dialogue_id: int) -> list[BlockModel]:
        blocks = await self._session.execute(
            select(BlockModel)
            .options(
                selectin_polymorphic(BlockModel, BlockModel.__subclasses__()),
            )
            .where(BlockModel.dialogue_id == dialogue_id)
            .order_by(BlockModel.sequence_number)
        )
        return blocks.unique().scalars().all()

    async def get_block(self, block_id: int) -> Optional[BlockReadDTO]:
        block_model = await self._get_block_model_instance(block_id)
        if block_model is None:
            return None
        return block_model.to_dto()

    async def _get_block_model_instance(self, block_id: int) -> Optional[BlockModel]:
        block = await self._session.execute(
            select(BlockModel)
            .options(
                selectin_polymorphic(BlockModel, BlockModel.__subclasses__()),
            )
            .where(BlockModel.block_id == block_id)
        )
        return block.scalar()

    async def update_block(
        self,
        dialogue_id: int,
        block_id: int,
        block: BlockUpdateDTO,
    ) -> Optional[BlockReadDTO]:
        existing_block = await self._get_block_model_instance(block_id)

        for key, value in block.__dict__.items():
            setattr(existing_block, key, value)

        await self._update_blocks_sequence_numbers_without_commit(dialogue_id)
        await self._session.commit()

        return existing_block.to_dto()

    async def _update_blocks_sequence_numbers_without_commit(self, dialogue_id: int) -> list[BlockReadDTO]:
        blocks = await self._get_blocks(dialogue_id)
        blocks_to_return = []
        for counter, block in enumerate(sorted(blocks, key=lambda x: x.sequence_number), start=1):
            block.sequence_number = counter
            blocks_to_return.append(block.to_dto())
        return blocks_to_return

    async def delete_block(self, dialogue_id: int, block_id: int) -> Optional[BlockReadDTO]:
        await self._session.execute(delete(BlockModel).where(BlockModel.block_id == block_id))
        await self._update_blocks_sequence_numbers_without_commit(dialogue_id)
        await self._session.commit()
