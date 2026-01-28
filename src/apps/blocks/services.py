import os
from uuid import UUID

from fastapi import UploadFile

from src.apps.blocks.dependencies.repositories_dependencies import BlockRepositoryDI
from src.apps.dialogues.dependencies.services_dependencies import DialogueServiceDI
from src.apps.enums import BlockType
from src.apps.blocks.schemas import (
    UnionBlockCreateSchema,
    UnionBlockReadSchema,
    UnionBlockUpdateSchema,
    ImageBlockReadSchema,
)
from src.apps.blocks.exceptions.services_exceptions import BlockNotFoundError, InvalidBlockTypeError


class BlockService:
    def __init__(
        self,
        block_repository: BlockRepositoryDI,
        dialogue_service: DialogueServiceDI,
    ):
        self._block_repository = block_repository
        self._dialogue_service = dialogue_service

    async def create_block(
        self,
        user_id: UUID,
        project_id: int,
        dialogue_id: int,
        block_data: UnionBlockCreateSchema,
    ) -> UnionBlockReadSchema:
        await self._dialogue_service.raise_error_if_not_exists(user_id, project_id, dialogue_id)
        return await self._block_repository.create_block(dialogue_id, block_data)

    async def get_blocks(
        self,
        user_id: UUID,
        project_id: int,
        dialogue_id: int,
    ) -> list[UnionBlockReadSchema]:
        await self._dialogue_service.raise_error_if_not_exists(user_id, project_id, dialogue_id)
        blocks = await self._block_repository.get_blocks(dialogue_id)
        blocks.sort(key=lambda x: x.sequence_number)
        return blocks

    async def upload_image_for_image_block(
        self,
        user_id: UUID,
        project_id: int,
        dialogue_id: int,
        block_id: int,
        image: UploadFile,
    ) -> ImageBlockReadSchema:
        block_read = await self.get_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
        )
        if block_read.type != BlockType.IMAGE_BLOCK.value:
            raise InvalidBlockTypeError

        if block_read.image_path:
            full_image_path = os.path.join('src', 'media', block_read.image_path)
            if os.path.exists(full_image_path):
                os.remove(full_image_path)

        # TODO: use os.path.join
        image_path = f'src/media/users/{user_id}/projects/{project_id}/dialogues/{dialogue_id}/{image.filename}'
        if not os.path.exists(os.path.dirname(image_path)):
            os.makedirs(os.path.dirname(image_path))

        with open(image_path, 'wb+') as buffer:
            buffer.write(image.file.read())

        block_update = ImageBlockReadSchema(
            **{field_name: getattr(block_read, field_name) for field_name in ImageBlockReadSchema.__fields__}
        )
        # TODO: use os.path.join
        block_update.image_path = image_path.replace('src/media/', '')

        return await self.update_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
            block_data=block_update,
        )

    async def update_block(
        self,
        user_id: UUID,
        project_id: int,
        dialogue_id: int,
        block_id: int,
        block_data: UnionBlockUpdateSchema,
    ) -> UnionBlockReadSchema:
        await self.raise_error_if_not_exists(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
        )
        return await self._block_repository.update_block(
            dialogue_id=dialogue_id,
            block_id=block_id,
            block_data=block_data,
        )

    async def delete_block(
        self,
        user_id: UUID,
        project_id: int,
        dialogue_id: int,
        block_id: int,
    ) -> UnionBlockReadSchema:
        block = await self.get_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
        )
        if block.type == BlockType.IMAGE_BLOCK.value and block.image_path:
            full_image_path = os.path.join('src', 'media', block.image_path)
            if os.path.exists(full_image_path):
                os.remove(full_image_path)

        await self._block_repository.delete_block(dialogue_id, block_id)

    # TODO: refactor, use repo method
    async def get_block(
        self,
        user_id: UUID,
        project_id: int,
        dialogue_id: int,
        block_id: int,
    ) -> UnionBlockReadSchema:
        blocks = await self.get_blocks(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
        )

        block_with_specified_id = [block for block in blocks if block.block_id == block_id]
        if not block_with_specified_id:
            raise BlockNotFoundError

        return block_with_specified_id[0]

    async def raise_error_if_not_exists(self, user_id: UUID, project_id: int, dialogue_id: int, block_id: int):
        await self._dialogue_service.raise_error_if_not_exists(user_id, project_id, dialogue_id)
        if not await self._block_repository.exists_by_id(dialogue_id, block_id):
            raise BlockNotFoundError
