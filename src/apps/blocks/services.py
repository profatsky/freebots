from uuid import UUID

from fastapi import UploadFile

from src.apps.blocks.dependencies.repositories_dependencies import BlockRepositoryDI
from src.apps.blocks.dto.base import BlockCreateDTO, BlockReadDTO, BlockUpdateDTO
from src.apps.blocks.dto.image import ImageBlockUpdateDTO, ImageBlockReadDTO
from src.apps.dialogues.dependencies.services_dependencies import DialogueServiceDI
from src.apps.enums import BlockType
from src.apps.blocks.errors import BlockNotFoundError, InvalidBlockTypeError
from src.core.config import MEDIA_DIR
from src.core.utils import soft_delete_file


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
        block: BlockCreateDTO,
    ) -> BlockReadDTO:
        _ = await self._dialogue_service.get_dialogue(user_id=user_id, project_id=project_id, dialogue_id=dialogue_id)
        return await self._block_repository.create_block(dialogue_id=dialogue_id, block=block)

    async def get_blocks(self, user_id: UUID, project_id: int, dialogue_id: int) -> list[BlockReadDTO]:
        _ = await self._dialogue_service.get_dialogue(user_id=user_id, project_id=project_id, dialogue_id=dialogue_id)
        return await self._block_repository.get_blocks(dialogue_id)

    async def get_block(
        self,
        user_id: UUID,
        project_id: int,
        dialogue_id: int,
        block_id: int,
    ) -> BlockReadDTO:
        _ = await self._dialogue_service.get_dialogue(user_id=user_id, project_id=project_id, dialogue_id=dialogue_id)
        block = await self._block_repository.get_block(block_id)
        if block is None:
            raise BlockNotFoundError
        return block

    async def upload_image_for_image_block(
        self,
        user_id: UUID,
        project_id: int,
        dialogue_id: int,
        block_id: int,
        image: UploadFile,
    ) -> ImageBlockReadDTO:
        block = await self.get_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
        )
        if block.type != BlockType.IMAGE_BLOCK.value:
            raise InvalidBlockTypeError

        # TODO: fix type hint warning
        if block.image_path:
            await soft_delete_file(MEDIA_DIR / block.image_path)

        image_path = MEDIA_DIR / f'users/{user_id}/projects/{project_id}/dialogues/{dialogue_id}/{image.filename}'

        # TODO: async
        if not image_path.parent.exists():
            image_path.parent.mkdir(parents=True)

        # TODO: async
        with open(image_path, 'wb+') as buffer:
            buffer.write(image.file.read())

        block_to_update = ImageBlockUpdateDTO(
            type=block.type,
            image_path=str(image_path.relative_to(MEDIA_DIR)),
        )

        # TODO: fix type hint warning
        return await self.update_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
            block=block_to_update,
        )

    async def update_block(
        self,
        user_id: UUID,
        project_id: int,
        dialogue_id: int,
        block_id: int,
        block: BlockUpdateDTO,
    ) -> BlockReadDTO:
        _ = await self.get_block(user_id=user_id, project_id=project_id, dialogue_id=dialogue_id, block_id=block_id)
        return await self._block_repository.update_block(dialogue_id=dialogue_id, block_id=block_id, block=block)

    async def delete_block(
        self,
        user_id: UUID,
        project_id: int,
        dialogue_id: int,
        block_id: int,
    ):
        block = await self.get_block(user_id=user_id, project_id=project_id, dialogue_id=dialogue_id, block_id=block_id)
        # TODO: fix type hint warning
        if block.type == BlockType.IMAGE_BLOCK.value and block.image_path:
            await soft_delete_file(MEDIA_DIR / block.image_path)

        await self._block_repository.delete_block(dialogue_id, block_id)
