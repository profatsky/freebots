from fastapi import APIRouter

from src.apps.auth.api import router as auth_router
from src.api.v1.users.endpoints import router as users_router
from src.apps.projects.api import router as projects_router
from src.apps.dialogues.api import router as dialogues_router
from src.apps.dialogue_templates.api import router as dialogue_templates_router
from src.apps.blocks.api import router as blocks_router
from src.apps.plugins.api import router as plugins_router
from src.apps.code_gen.api import router as code_gen_router
from src.apps.statistics.api import router as statistics_router
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
