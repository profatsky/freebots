from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Header, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.apps.auth.dependencies.services_dependencies import AuthServiceDI
from src.api.v1.auth.exceptions import InvalidCodeHTTPException, ExpiredCodeHTTPException
from src.apps.auth.errors import InvalidCodeError, ExpiredCodeError
from src.api.v1.auth.schemas import TelegramCredentialsSchema
from src.core.config import settings

router = APIRouter(tags=['Auth'])


@router.post('/save_tg_code', status_code=status.HTTP_201_CREATED)
async def save_tg_code(
    auth_service: AuthServiceDI,
    tg_credentials: TelegramCredentialsSchema,
    x_bot_secret: str = Header(alias='X-BOT-SECRET'),
):
    if x_bot_secret != settings.AUTH_BOT_SECRET:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid bot secret')

    await auth_service.save_tg_code(tg_id=tg_credentials.tg_id, code=tg_credentials.code)
    return {'detail': 'Code saved'}


@router.post('/swagger_login')
async def login_via_swagger(
    auth_service: AuthServiceDI,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    if settings.DEBUG:
        access_token = await auth_service.register_or_login(tg_id=0, is_superuser=True)
        return {'access_token': access_token, 'token_type': 'bearer'}
    return await _login_via_telegram(auth_service=auth_service, code=int(form_data.password))


@router.post('/login_via_telegram', status_code=status.HTTP_200_OK)
async def login_via_telegram(
    auth_service: AuthServiceDI,
    code: Annotated[int, Body(embed=True)],
):
    return await _login_via_telegram(code=code, auth_service=auth_service)


async def _login_via_telegram(
    auth_service: AuthServiceDI,
    code: Annotated[int, Body(embed=True)],
):
    try:
        tg_id = await auth_service.get_tg_id_by_code(code)
    except InvalidCodeError:
        raise InvalidCodeHTTPException
    except ExpiredCodeError:
        raise ExpiredCodeHTTPException

    access_token = await auth_service.register_or_login(tg_id)
    return {'access_token': access_token, 'token_type': 'bearer'}
