from typing import Annotated

from authx import TokenPayload, AuthX
from fastapi import Depends, Request


def get_auth_security(request: Request):
    return request.state.auth_security


AuthSecurityDI = Annotated[AuthX, Depends(get_auth_security)]


async def access_token_required(request: Request, auth_security: AuthSecurityDI) -> TokenPayload:
    auth_required = auth_security.token_required()
    token = await auth_required(request)
    return token


async def get_user_id_from_subject(request: Request, auth_security: AuthSecurityDI) -> int:
    token = await auth_security.get_access_token_from_request(request)
    token_payload = auth_security.verify_token(token)
    return int(token_payload.sub)


UserIDFromAccessTokenDI = Annotated[int, Depends(get_user_id_from_subject)]
