from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Header, Request, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.apps.auth.dependencies.services_dependencies import AuthServiceDI
from src.apps.auth.schemas import TelegramCredentialsSchema
from src.core.config import settings

router = APIRouter(tags=['Auth'])

CODE_TTL = 300


@router.post('/swagger_login')
async def login_via_swagger(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDI,
):
    if settings.DEBUG:
        access_token = await auth_service.register_or_login(tg_id=0, is_superuser=True)
        return {'access_token': access_token, 'token_type': 'bearer'}
    return await _login_via_telegram(request=request, auth_service=auth_service, code=int(form_data.password))


# TODO: service and repository layers
@router.post('/save_tg_code', status_code=status.HTTP_201_CREATED)
async def save_tg_code(
    request: Request,
    tg_credentials: TelegramCredentialsSchema,
    x_bot_secret: str = Header(alias='X-BOT-SECRET'),
):
    if x_bot_secret != settings.AUTH_BOT_SECRET:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid bot secret')

    cache_client = request.state.cache_cli

    key = f'tg_code:{tg_credentials.code}'
    await cache_client.set(name=key, value=tg_credentials.tg_id, ex=CODE_TTL)
    return {'detail': 'Code saved'}


# TODO: service and repository layers
@router.post('/login_via_telegram', status_code=status.HTTP_200_OK)
async def login_via_telegram(
    request: Request,
    code: Annotated[int, Body(embed=True)],
    auth_service: AuthServiceDI,
):
    return await _login_via_telegram(request=request, code=code, auth_service=auth_service)


async def _login_via_telegram(
    request: Request,
    code: Annotated[int, Body(embed=True)],
    auth_service: AuthServiceDI,
):
    cache_cli = request.state.cache_cli

    key = f'tg_code:{code}'
    stored_tg_id = await cache_cli.get(key)
    if stored_tg_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный код')

    ttl = await cache_cli.ttl(key)
    if ttl == -1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Код истек')

    await cache_cli.delete(key)

    access_token = await auth_service.register_or_login(int(stored_tg_id.decode()))
    return {'access_token': access_token, 'token_type': 'bearer'}
