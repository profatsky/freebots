from fastapi import APIRouter, status, Depends

from src.api.v1.dialogues.schemas.dialogues import DialogueReadSchema, DialogueCreateSchema
from src.api.v1.dialogues.schemas.triggers import DialogueTriggerUpdateSchema
from src.apps.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.apps.dialogues.dependencies.services_dependencies import DialogueServiceDI
from src.api.v1.dialogues.exceptions import (
    DialoguesLimitExceededHTTPException,
    DialogueNotFoundHTTPException,
)
from src.apps.dialogues.errors import DialoguesLimitExceededError, DialogueNotFoundError
from src.api.v1.projects.exceptions import (
    ProjectNotFoundHTTPException,
    NoPermissionForProjectHTTPException,
)
from src.apps.projects.errors import ProjectNotFoundError, NoPermissionForProjectError

router = APIRouter(
    prefix='/projects/{project_id}/dialogues',
    tags=['Dialogues'],
    dependencies=[Depends(access_token_required)],
)


@router.post(
    '',
    response_model=DialogueReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_dialogue(
    dialogue_service: DialogueServiceDI,
    project_id: int,
    dialogue: DialogueCreateSchema,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        dialogue = await dialogue_service.create_dialogue(
            user_id=user_id,
            dialogue=dialogue.to_dto(project_id=project_id),
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException
    except DialoguesLimitExceededError:
        raise DialoguesLimitExceededHTTPException
    return DialogueReadSchema.from_dto(dialogue)


@router.put(
    '/{dialogue_id}',
    response_model=DialogueReadSchema,
)
async def update_dialogue_trigger(
    dialogue_service: DialogueServiceDI,
    project_id: int,
    dialogue_id: int,
    trigger: DialogueTriggerUpdateSchema,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        dialogue = await dialogue_service.update_dialogue_trigger(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            trigger=trigger.to_dto(),
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException
    except DialogueNotFoundError:
        raise DialogueNotFoundHTTPException
    return DialogueReadSchema.from_dto(dialogue)


@router.delete(
    '/{dialogue_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_dialogue(
    dialogue_service: DialogueServiceDI,
    project_id: int,
    dialogue_id: int,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        await dialogue_service.delete_dialogue(
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
