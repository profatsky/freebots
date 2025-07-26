from fastapi import APIRouter, status

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
