from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.orm import selectin_polymorphic

from src.blocks.models import BlockModel
from src.blocks.schemas import UnionBlockCreateSchema, UnionBlockReadSchema, UnionBlockUpdateSchema
from src.blocks import utils
from src.core.base_repository import BaseRepository


class BlockRepository(BaseRepository):
    async def create_block(
        self,
        dialogue_id: int,
        block_data: UnionBlockCreateSchema,
    ) -> UnionBlockReadSchema:
        blocks = await self.get_blocks(dialogue_id)
        blocks_number = len(blocks)

        block_model = utils.get_block_model_by_type(block_data.type)
        block = block_model(**block_data.model_dump(), dialogue_id=dialogue_id, sequence_number=blocks_number + 1)
        self._session.add(block)
        await self._session.commit()

        return utils.validate_block_from_db(block)

    async def get_blocks(self, dialogue_id: int) -> list[UnionBlockReadSchema]:
        blocks = await self._get_blocks(dialogue_id)
        return [utils.validate_block_from_db(block) for block in blocks]

    async def _get_blocks(self, dialogue_id: int) -> list[utils.UnionBlockModel]:
        blocks = await self._session.execute(
            select(BlockModel)
            .options(
                selectin_polymorphic(BlockModel, BlockModel.__subclasses__()),
            )
            .where(BlockModel.dialogue_id == dialogue_id)
            .order_by(BlockModel.sequence_number)
        )
        return blocks.unique().scalars().all()

    async def _get_block_model_instance(self, block_id: int) -> Optional[utils.UnionBlockModel]:
        block = await self._session.execute(select(BlockModel).where(BlockModel.block_id == block_id))
        return block.scalar()

    async def update_block(
        self,
        dialogue_id: int,
        block_id: int,
        block_data: UnionBlockUpdateSchema,
    ) -> Optional[UnionBlockReadSchema]:
        block = await self._get_block_model_instance(block_id)

        for key, value in block_data.model_dump().items():
            setattr(block, key, value)

        await self._update_blocks_sequence_numbers_without_commit(dialogue_id)
        await self._session.commit()

        return utils.validate_block_from_db(block)

    async def _update_blocks_sequence_numbers_without_commit(self, dialogue_id: int) -> Optional[UnionBlockReadSchema]:
        blocks = await self._get_blocks(dialogue_id)
        counter = 1
        for block in sorted(blocks, key=lambda x: x.sequence_number):
            block.sequence_number = counter
            counter += 1

        return [utils.validate_block_from_db(block) for block in blocks]

    async def delete_block(self, dialogue_id: int, block_id: int) -> Optional[UnionBlockReadSchema]:
        await self._session.execute(delete(BlockModel).where(BlockModel.block_id == block_id))
        await self._update_blocks_sequence_numbers_without_commit(dialogue_id)
        await self._session.commit()
