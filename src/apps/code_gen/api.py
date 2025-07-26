from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from src.apps.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.apps.code_gen.dependencies.services_dependencies import CodeGenServiceDI
from src.apps.dialogues.exceptions.http_exceptions import NoDialoguesInProjectHTTPException
from src.apps.dialogues.exceptions.services_exceptions import NoDialoguesInProjectError
from src.apps.dialogues.schemas import DialogueWithBlocksReadSchema
from src.apps.projects.exceptions.http_exceptions import (
    ProjectNotFoundHTTPException,
    NoPermissionForProjectHTTPException,
)
from src.apps.projects.exceptions.services_exceptions import ProjectNotFoundError, NoPermissionForProjectError

router = APIRouter(
    prefix='/projects',
    tags=['Projects'],
    dependencies=[Depends(access_token_required)],
)


@router.get(
    '/{project_id}/code',
    response_model=list[DialogueWithBlocksReadSchema],
)
async def get_bot_code(
    project_id: int,
    code_gen_service: CodeGenServiceDI,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        zipped_bot = await code_gen_service.get_bot_code_in_zip(
            user_id=user_id,
            project_id=project_id,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except NoDialoguesInProjectError:
        raise NoDialoguesInProjectHTTPException

    return StreamingResponse(
        content=zipped_bot,
        media_type='application/zip',
        headers={
            'Content-Disposition': 'attachment; filename=bot.zip',
        },
    )
