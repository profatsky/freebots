from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError

from src.apps.auth.dependencies.services_dependencies import AuthServiceDI
from src.apps.auth.exceptions.http_exception import InvalidCredentialsHTTPException
from src.apps.auth.schemas import AuthCredentialsSchema
from src.apps.users.exceptions.http_exceptions import UserAlreadyExistsHTTPException
from src.apps.users.exceptions.services_exceptions import UserAlreadyExistsError
from src.apps.auth.exceptions.services_exceptions import InvalidCredentialsError

router = APIRouter(tags=['Auth'])


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(
    credentials: AuthCredentialsSchema,
    auth_service: AuthServiceDI,
):
    try:
        access_token = await auth_service.register(credentials)
    except UserAlreadyExistsError:
        raise UserAlreadyExistsHTTPException

    return {
        'detail': 'Registration was successful',
        'access_token': access_token,
    }


@router.post('/login')
async def login(
    credentials: AuthCredentialsSchema,
    auth_service: AuthServiceDI,
):
    try:
        access_token = await auth_service.login(credentials)
    except InvalidCredentialsError:
        raise InvalidCredentialsHTTPException

    return {
        'detail': 'Authorization was successful',
        'access_token': access_token,
    }


@router.post('/swagger_login')
async def login_via_swagger(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDI,
):
    try:
        credentials = AuthCredentialsSchema(
            email=form_data.username,
            password=form_data.password,
        )
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.errors())

    try:
        access_token = await auth_service.login(credentials)
    except InvalidCredentialsError:
        raise InvalidCredentialsHTTPException

    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }
