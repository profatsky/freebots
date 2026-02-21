from typing import Annotated

from fastapi import APIRouter, Query, status, Body, Depends

from src.apps.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.apps.dialogue_templates.dependencies.services_dependencies import DialogueTemplateServiceDI
from src.api.v1.dialogue_templates.exceptions import DialogueTemplateNotFoundHTTPException
from src.apps.dialogue_templates.errors import DialogueTemplateNotFoundError
from src.api.v1.dialogue_templates.schemas import DialogueTemplateReadSchema
from src.api.v1.dialogues.exceptions import DialoguesLimitExceededHTTPException
from src.apps.dialogues.errors import DialoguesLimitExceededError
from src.api.v1.projects.exceptions import (
    ProjectNotFoundHTTPException,
    NoPermissionForProjectHTTPException,
)
from src.apps.projects.errors import ProjectNotFoundError, NoPermissionForProjectError

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
    templates = await dialogue_template_service.get_templates(page)
    return [DialogueTemplateReadSchema.from_dto(template) for template in templates]


@router.get(
    '/templates/{template_id}',
    response_model=DialogueTemplateReadSchema,
)
async def get_dialogue_template(
    dialogue_template_service: DialogueTemplateServiceDI,
    template_id: int,
):
    try:
        template = await dialogue_template_service.get_template(template_id)
    except DialogueTemplateNotFoundError:
        raise DialogueTemplateNotFoundHTTPException
    return DialogueTemplateReadSchema.from_dto(template)


@router.post(
    '/projects/{project_id}/templates',
    status_code=status.HTTP_201_CREATED,
)
async def add_dialogue_template_to_project(
    dialogue_template_service: DialogueTemplateServiceDI,
    project_id: int,
    template_id: Annotated[int, Body(embed=True)],
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
