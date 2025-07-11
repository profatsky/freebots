from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from src.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.code_gen.dependencies.services_dependencies import CodeGenServiceDI
from src.dialogues.exceptions.http_exceptions import NoDialoguesInProjectHTTPException
from src.dialogues.exceptions.services_exceptions import NoDialoguesInProjectError
from src.dialogues.schemas import DialogueWithBlocksReadSchema
from src.projects.exceptions.http_exceptions import ProjectNotFoundHTTPException, NoPermissionForProjectHTTPException
from src.projects.exceptions.services_exceptions import ProjectNotFoundError, NoPermissionForProjectError

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
