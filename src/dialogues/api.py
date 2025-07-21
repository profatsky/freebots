from fastapi import APIRouter, status, Depends

from src.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.dialogues.dependencies.services_dependencies import DialogueServiceDI
from src.dialogues.exceptions.http_exceptions import DialoguesLimitExceededHTTPException, DialogueNotFoundHTTPException
from src.dialogues.exceptions.services_exceptions import DialoguesLimitExceededError, DialogueNotFoundError
from src.dialogues.schemas import DialogueCreateSchema, DialogueReadSchema, TriggerUpdateSchema
from src.projects.exceptions.http_exceptions import ProjectNotFoundHTTPException, NoPermissionForProjectHTTPException
from src.projects.exceptions.services_exceptions import ProjectNotFoundError, NoPermissionForProjectError

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
    project_id: int,
    dialogue_data: DialogueCreateSchema,
    dialogue_service: DialogueServiceDI,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        return await dialogue_service.create_dialogue(
            user_id=user_id,
            project_id=project_id,
            dialogue_data=dialogue_data,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except DialoguesLimitExceededError:
        raise DialoguesLimitExceededHTTPException


@router.put(
    '/{dialogue_id}',
    response_model=DialogueReadSchema,
)
async def update_dialogue_trigger(
    project_id: int,
    dialogue_id: int,
    trigger: TriggerUpdateSchema,
    dialogue_service: DialogueServiceDI,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        return await dialogue_service.update_dialogue_trigger(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            trigger=trigger,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except DialogueNotFoundError:
        raise DialogueNotFoundHTTPException


@router.delete(
    '/{dialogue_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_dialogue(
    project_id: int,
    dialogue_id: int,
    dialogue_service: DialogueServiceDI,
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
