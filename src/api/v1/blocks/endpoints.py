from typing import Annotated

from fastapi import APIRouter, status, UploadFile, Depends, Body

from src.api.v1.blocks.schemas import (
    UnionBlockReadSchema,
    UnionBlockCreateSchema,
    UnionBlockUpdateSchema,
    ImageBlockReadSchema,
)
from src.api.v1.blocks.utils import convert_block_read_dto_to_schema
from src.apps.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.apps.blocks.dependencies.services_dependencies import BlockServiceDI
from src.api.v1.blocks.exceptions import (
    RepeatingBlockSequenceNumberHTTPException,
    BlockNotFoundHTTPException,
    InvalidBlockTypeHTTPException,
)
from src.apps.blocks.errors import (
    RepeatingBlockSequenceNumberError,
    BlockNotFoundError,
    InvalidBlockTypeError,
)
from src.api.v1.blocks.openapi_examples import BLOCK_CREATE_SCHEMA_EXAMPLES, BLOCK_UPDATE_SCHEMA_EXAMPLES
from src.api.v1.dialogues.exceptions import DialogueNotFoundHTTPException
from src.apps.dialogues.errors import DialogueNotFoundError
from src.apps.projects.errors import ProjectNotFoundError, NoPermissionForProjectError
from src.api.v1.projects.exceptions import (
    ProjectNotFoundHTTPException,
    NoPermissionForProjectHTTPException,
)

router = APIRouter(
    prefix='/projects/{project_id}/dialogues/{dialogue_id}/blocks',
    tags=['Blocks'],
    dependencies=[Depends(access_token_required)],
)


@router.post(
    '',
    response_model=UnionBlockReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_block(
    block_service: BlockServiceDI,
    project_id: int,
    dialogue_id: int,
    block: Annotated[
        UnionBlockCreateSchema,
        Body(openapi_examples=BLOCK_CREATE_SCHEMA_EXAMPLES),
    ],
    user_id: UserIDFromAccessTokenDI,
):
    try:
        block = await block_service.create_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block=block.to_dto(),
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException
    except DialogueNotFoundError:
        raise DialogueNotFoundHTTPException
    except RepeatingBlockSequenceNumberError:
        raise RepeatingBlockSequenceNumberHTTPException
    return convert_block_read_dto_to_schema(block)


@router.get(
    '',
    response_model=list[UnionBlockReadSchema],
)
async def get_blocks(
    block_service: BlockServiceDI,
    project_id: int,
    dialogue_id: int,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        blocks = await block_service.get_blocks(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException
    except DialogueNotFoundError:
        raise DialogueNotFoundHTTPException
    return [convert_block_read_dto_to_schema(block) for block in blocks]


@router.put(
    '/{block_id}',
    response_model=UnionBlockReadSchema,
)
async def update_block(
    block_service: BlockServiceDI,
    project_id: int,
    dialogue_id: int,
    block_id: int,
    block: Annotated[
        UnionBlockUpdateSchema,
        Body(openapi_examples=BLOCK_UPDATE_SCHEMA_EXAMPLES),
    ],
    user_id: UserIDFromAccessTokenDI,
):
    try:
        block = await block_service.update_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
            block=block.to_dto(),
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException
    except DialogueNotFoundError:
        raise DialogueNotFoundHTTPException
    except BlockNotFoundError:
        raise BlockNotFoundHTTPException
    except RepeatingBlockSequenceNumberError:
        raise RepeatingBlockSequenceNumberHTTPException
    return convert_block_read_dto_to_schema(block)


@router.post(
    '/{block_id}/upload-image',
    response_model=ImageBlockReadSchema,
)
async def upload_image_for_image_block(
    block_service: BlockServiceDI,
    project_id: int,
    dialogue_id: int,
    block_id: int,
    image: UploadFile,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        block = await block_service.upload_image_for_image_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
            image=image,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException
    except DialogueNotFoundError:
        raise DialogueNotFoundHTTPException
    except BlockNotFoundError:
        raise BlockNotFoundHTTPException
    except InvalidBlockTypeError:
        raise InvalidBlockTypeHTTPException
    return ImageBlockReadSchema.from_dto(block)


@router.delete(
    '/{block_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_block(
    block_service: BlockServiceDI,
    project_id: int,
    dialogue_id: int,
    block_id: int,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        await block_service.delete_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException
    except DialogueNotFoundError:
        raise DialogueNotFoundHTTPException
    except BlockNotFoundError:
        raise BlockNotFoundHTTPException
