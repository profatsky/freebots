from fastapi import APIRouter

from src.auth.api import router as auth_router
from src.users.api import router as users_router
from src.projects.api import router as projects_router
from src.dialogues.api import router as dialogues_router
from src.dialogue_templates.api import router as dialogue_templates_router
from src.blocks.api import router as blocks_router
from src.plugins.api import router as plugins_router
from src.code_gen.api import router as code_gen_router
from src.statistics.api import router as statistics_router


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
    ]

    for router in routers:
        app_router.include_router(router)

    return app_router
