from typing import Annotated
from uuid import UUID

from authx import TokenPayload, AuthX
from fastapi import Depends, Request, HTTPException, status

from src.core.config import oauth2_scheme


def get_auth_security(request: Request):
    return request.state.auth_security


AuthSecurityDI = Annotated[AuthX, Depends(get_auth_security)]


async def access_token_required(
    request: Request, auth_security: AuthSecurityDI, _: Annotated[str, Depends(oauth2_scheme)]
) -> TokenPayload:
    auth_required = auth_security.token_required()
    token = await auth_required(request)
    return token


async def get_user_id_from_subject(request: Request, auth_security: AuthSecurityDI) -> UUID:
    token = await auth_security.get_access_token_from_request(request)
    token_payload = auth_security.verify_token(token)
    try:
        return UUID(token_payload.sub)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


UserIDFromAccessTokenDI = Annotated[UUID, Depends(get_user_id_from_subject)]
