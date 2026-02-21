from fastapi import APIRouter

from src.api.v1.auth.endpoints import router as auth_router
from src.api.v1.users.endpoints import router as users_router
from src.api.v1.projects.endpoints import router as projects_router
from src.api.v1.dialogues.endpoints import router as dialogues_router
from src.api.v1.dialogue_templates.endpoints import router as dialogue_templates_router
from src.apps.blocks.api import router as blocks_router
from src.api.v1.plugins.endpoints import router as plugins_router
from src.apps.code_gen.api import router as code_gen_router
from src.api.v1.statistics.endpoints import router as statistics_router
from src.apps.subscriptions.api import router as subscriptions_router

try:
    from src.apps.payments.api import router as payments_router
except ImportError:
    payments_router = APIRouter(prefix='/payments', tags=['payments'])


def get_app_router() -> APIRouter:
    app_router = APIRouter(prefix='/api')

    routers = [
        auth_router,
        users_router,
        projects_router,
        dialogues_router,
        dialogue_templates_router,
        blocks_router,
        plugins_router,
        code_gen_router,
        statistics_router,
        subscriptions_router,
        payments_router,
    ]

    for router in routers:
        app_router.include_router(router)

    return app_router
