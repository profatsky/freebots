from typing import Annotated

from fastapi import APIRouter, status, UploadFile, Depends, Body

from src.apps.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.apps.blocks.dependencies.services_dependencies import BlockServiceDI
from src.apps.blocks.exceptions.http_exceptions import (
    RepeatingBlockSequenceNumberHTTPException,
    BlockNotFoundHTTPException,
    InvalidBlockTypeHTTPException,
)
from src.apps.blocks.exceptions.services_exceptions import (
    RepeatingBlockSequenceNumberError,
    BlockNotFoundError,
    InvalidBlockTypeError,
)
from src.apps.blocks.openapi_examples import BLOCK_CREATE_SCHEMA_EXAMPLES, BLOCK_UPDATE_SCHEMA_EXAMPLES
from src.apps.blocks.schemas import UnionBlockCreateSchema, UnionBlockReadSchema, UnionBlockUpdateSchema
from src.apps.dialogues.exceptions.http_exceptions import DialogueNotFoundHTTPException
from src.apps.dialogues.exceptions.services_exceptions import DialogueNotFoundError
from src.apps.projects.exceptions.services_exceptions import ProjectNotFoundError, NoPermissionForProjectError
from src.apps.projects.exceptions.http_exceptions import (
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
    project_id: int,
    dialogue_id: int,
    block: Annotated[
        UnionBlockCreateSchema,
        Body(openapi_examples=BLOCK_CREATE_SCHEMA_EXAMPLES),
    ],
    block_service: BlockServiceDI,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        return await block_service.create_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_data=block,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except DialogueNotFoundError:
        raise DialogueNotFoundHTTPException

    except RepeatingBlockSequenceNumberError:
        raise RepeatingBlockSequenceNumberHTTPException


@router.get(
    '',
    response_model=list[UnionBlockReadSchema],
)
async def get_blocks(
    project_id: int,
    dialogue_id: int,
    block_service: BlockServiceDI,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        return await block_service.get_blocks(
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


@router.put(
    '/{block_id}',
    response_model=UnionBlockReadSchema,
)
async def update_block(
    project_id: int,
    dialogue_id: int,
    block_id: int,
    block: Annotated[
        UnionBlockUpdateSchema,
        Body(openapi_examples=BLOCK_UPDATE_SCHEMA_EXAMPLES),
    ],
    block_service: BlockServiceDI,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        return await block_service.update_block(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            block_id=block_id,
            block_data=block,
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


@router.post(
    '/{block_id}/upload-image',
    response_model=UnionBlockReadSchema,
)
async def upload_image_for_image_block(
    project_id: int,
    dialogue_id: int,
    block_id: int,
    image: UploadFile,
    block_service: BlockServiceDI,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        return await block_service.upload_image_for_image_block(
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


@router.delete(
    '/{block_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_block(
    project_id: int,
    dialogue_id: int,
    block_id: int,
    block_service: BlockServiceDI,
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
