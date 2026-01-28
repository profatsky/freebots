from typing import Annotated

from fastapi import APIRouter, Query, status, Body, Depends

from src.apps.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.apps.dialogue_templates.dependencies.services_dependencies import DialogueTemplateServiceDI
from src.apps.dialogue_templates.exceptions.http_exceptions import DialogueTemplateNotFoundHTTPException
from src.apps.dialogue_templates.exceptions.services_exceptions import DialogueTemplateNotFoundError
from src.apps.dialogue_templates.schemas import DialogueTemplateReadSchema
from src.apps.dialogues.exceptions.http_exceptions import DialoguesLimitExceededHTTPException
from src.apps.dialogues.exceptions.services_exceptions import DialoguesLimitExceededError
from src.apps.projects.exceptions.http_exceptions import (
    ProjectNotFoundHTTPException,
    NoPermissionForProjectHTTPException,
)
from src.apps.projects.exceptions.services_exceptions import ProjectNotFoundError, NoPermissionForProjectError

router = APIRouter(
    tags=['Templates'],
    dependencies=[Depends(access_token_required)],
)


@router.get(
    '/templates',
    response_model=list[DialogueTemplateReadSchema],
)
async def get_dialogue_templates(
    dialogue_template_service: DialogueTemplateServiceDI,
    page: Annotated[int, Query(ge=1)] = 1,
):
    return await dialogue_template_service.get_templates(page)


@router.get(
    '/templates/{template_id}',
    response_model=DialogueTemplateReadSchema,
)
async def get_dialogue_template(
    template_id: int,
    dialogue_template_service: DialogueTemplateServiceDI,
):
    try:
        return await dialogue_template_service.get_template(template_id)
    except DialogueTemplateNotFoundError:
        raise DialogueTemplateNotFoundHTTPException


@router.post(
    '/projects/{project_id}/templates',
    status_code=status.HTTP_201_CREATED,
)
async def add_dialogue_template_to_project(
    project_id: int,
    template_id: Annotated[int, Body(embed=True)],
    dialogue_template_service: DialogueTemplateServiceDI,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        await dialogue_template_service.create_dialogue_from_template(
            user_id=user_id,
            project_id=project_id,
            template_id=template_id,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except DialogueTemplateNotFoundError:
        raise DialogueTemplateNotFoundHTTPException

    except DialoguesLimitExceededError:
        raise DialoguesLimitExceededHTTPException
