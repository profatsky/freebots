from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from src.apps.auth.dependencies.auth_dependencies import UserIDFromAccessTokenDI, access_token_required
from src.apps.ai_code_gen.dependencies.services_dependencies import AICodeGenServiceDI
from src.api.v1.ai_code_gen.schemas import (
    AICodeGenSessionCreateSchema,
    AICodeGenMessageCreateSchema,
    AICodeGenSessionWithMessagesReadSchema,
)
from src.api.v1.ai_code_gen.exceptions import (
    AICodeGenSessionNotFoundHTTPException,
    AICodeGenNoPermissionHTTPException,
    AICodeGenPromptTooLongHTTPException,
    AICodeGenMessagesLimitExceededHTTPException,
    AICodeGenInvalidResponseHTTPException,
    AICodeGenResponseTooLongHTTPException,
    AICodeGenNoAssistantMessageHTTPException,
)
from src.apps.ai_code_gen.errors import (
    AICodeGenSessionNotFoundError,
    AICodeGenSessionNoPermissionError,
    AICodeGenPromptTooLongError,
    AICodeGenMessagesLimitExceededError,
    AICodeGenInvalidResponseError,
    AICodeGenResponseTooLongError,
    AICodeGenNoAssistantMessageError,
)

router = APIRouter(
    prefix='/ai-code-gen',
    tags=['AI Code Gen'],
    dependencies=[Depends(access_token_required)],
)


@router.post('/sessions')
async def create_session(
    ai_code_gen_service: AICodeGenServiceDI,
    payload: AICodeGenSessionCreateSchema,
    user_id: UserIDFromAccessTokenDI,
) -> AICodeGenSessionWithMessagesReadSchema:
    try:
        session = await ai_code_gen_service.create_session(user_id=user_id, prompt=payload.prompt)
    except AICodeGenPromptTooLongError:
        raise AICodeGenPromptTooLongHTTPException
    except AICodeGenInvalidResponseError:
        raise AICodeGenInvalidResponseHTTPException
    except AICodeGenResponseTooLongError:
        raise AICodeGenResponseTooLongHTTPException
    return AICodeGenSessionWithMessagesReadSchema.from_dto(session)


@router.get('/sessions/{session_id}')
async def get_session(
    ai_code_gen_service: AICodeGenServiceDI,
    session_id: int,
    user_id: UserIDFromAccessTokenDI,
) -> AICodeGenSessionWithMessagesReadSchema:
    try:
        session = await ai_code_gen_service.get_session_with_messages(user_id=user_id, session_id=session_id)
    except AICodeGenSessionNotFoundError:
        raise AICodeGenSessionNotFoundHTTPException
    except AICodeGenSessionNoPermissionError:
        raise AICodeGenNoPermissionHTTPException
    return AICodeGenSessionWithMessagesReadSchema.from_dto(session)


@router.post('/sessions/{session_id}/messages')
async def add_message(
    ai_code_gen_service: AICodeGenServiceDI,
    session_id: int,
    payload: AICodeGenMessageCreateSchema,
    user_id: UserIDFromAccessTokenDI,
) -> AICodeGenSessionWithMessagesReadSchema:
    try:
        session = await ai_code_gen_service.add_message(
            user_id=user_id,
            session_id=session_id,
            prompt=payload.prompt,
        )
    except AICodeGenSessionNotFoundError:
        raise AICodeGenSessionNotFoundHTTPException
    except AICodeGenSessionNoPermissionError:
        raise AICodeGenNoPermissionHTTPException
    except AICodeGenPromptTooLongError:
        raise AICodeGenPromptTooLongHTTPException
    except AICodeGenMessagesLimitExceededError:
        raise AICodeGenMessagesLimitExceededHTTPException
    except AICodeGenInvalidResponseError:
        raise AICodeGenInvalidResponseHTTPException
    except AICodeGenResponseTooLongError:
        raise AICodeGenResponseTooLongHTTPException
    return AICodeGenSessionWithMessagesReadSchema.from_dto(session)


@router.get('/sessions/{session_id}/download')
async def download_code(
    ai_code_gen_service: AICodeGenServiceDI,
    session_id: int,
    user_id: UserIDFromAccessTokenDI,
):
    try:
        zip_data = await ai_code_gen_service.get_zip(user_id=user_id, session_id=session_id)
    except AICodeGenSessionNotFoundError:
        raise AICodeGenSessionNotFoundHTTPException
    except AICodeGenSessionNoPermissionError:
        raise AICodeGenNoPermissionHTTPException
    except AICodeGenNoAssistantMessageError:
        raise AICodeGenNoAssistantMessageHTTPException

    return StreamingResponse(
        content=zip_data,
        media_type='application/zip',
        headers={
            'Content-Disposition': 'attachment; filename=bot.zip',
        },
    )
