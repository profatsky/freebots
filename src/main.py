from contextlib import asynccontextmanager

import uvicorn as uvicorn
from authx import AuthX
from authx.exceptions import JWTDecodeError, MissingTokenError
from fastapi import FastAPI, HTTPException, status
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import src.core.config
from src.core.config import settings
from src.apps.router import get_app_router
from src.infrastructure.cache.client import CacheClient
from src.infrastructure.db.seeds.orm import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    auth_security = AuthX(config=src.core.config.auth_config)
    auth_security.handle_errors(app)

    await seed_database()

    async with CacheClient() as cache_client:
        yield {'auth_security': auth_security, 'cache_cli': cache_client}


app = FastAPI(title='Freebots', lifespan=lifespan)
app.mount('/api/media', StaticFiles(directory='src/media'), name='media')
app.include_router(get_app_router())

origins = [
    settings.CLIENT_APP_URL,
    *settings.YOOKASSA_IPS,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.exception_handler(JWTDecodeError)
async def jwt_decode_exception_handler(request: Request, exc: JWTDecodeError):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=exc.args[0],
    )


@app.exception_handler(MissingTokenError)
async def missing_access_token_exception_handler(request: Request, exc: MissingTokenError):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=exc.args[0],
    )


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        use_colors=True,
    )
