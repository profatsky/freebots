from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from src.apps.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.apps.code_gen.dependencies.services_dependencies import CodeGenServiceDI
from src.apps.dialogues.exceptions.http_exceptions import DialoguesLimitExceededHTTPException
from src.apps.dialogues.exceptions.services_exceptions import DialoguesLimitExceededError
from src.apps.dialogues.schemas import DialogueWithBlocksReadSchema
from src.api.v1.plugins.exceptions import PluginsNotAvailableForFreeUsersHTTPException
from src.apps.plugins.errors import PluginsNotAvailableForFreeUsersError
from src.api.v1.projects.exceptions import (
    ProjectNotFoundHTTPException,
    NoPermissionForProjectHTTPException,
)
from src.apps.projects.errors import ProjectNotFoundError, NoPermissionForProjectError
from src.apps.statistics.dependencies.services_dependencies import StatisticServiceDI

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
    statistic_service: StatisticServiceDI,
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

    except DialoguesLimitExceededError:
        raise DialoguesLimitExceededHTTPException

    except PluginsNotAvailableForFreeUsersError:
        raise PluginsNotAvailableForFreeUsersHTTPException

    await statistic_service.save_download_to_history(user_id=user_id, project_id=project_id)

    return StreamingResponse(
        content=zipped_bot,
        media_type='application/zip',
        headers={
            'Content-Disposition': 'attachment; filename=bot.zip',
        },
    )
