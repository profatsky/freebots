from uuid import UUID

from src.apps.dialogue_templates.dependencies.repositories_dependencies import DialogueTemplateRepositoryDI
from src.apps.dialogue_templates.dto import DialogueTemplateReadDTO
from src.apps.dialogue_templates.errors import DialogueTemplateNotFoundError
from src.apps.dialogues.errors import DialoguesLimitExceededError
from src.apps.projects.dependencies.services_dependencies import ProjectServiceDI
from src.apps.subscriptions.dependencies.services_dependencies import SubscriptionServiceDI
from src.core.consts import MAX_DIALOGUES_WITH_FREE_PLAN, MAX_DIALOGUES_WITH_PRO_PLAN

DIALOGUE_TEMPLATES_PER_PAGE = 9


class DialogueTemplateService:
    def __init__(
        self,
        dialogue_template_repository: DialogueTemplateRepositoryDI,
        project_service: ProjectServiceDI,
        subscription_service: SubscriptionServiceDI,
    ):
        self._dialogue_template_repository = dialogue_template_repository
        self._project_service = project_service
        self._subscription_service = subscription_service

    async def get_templates(self, page: int) -> list[DialogueTemplateReadDTO]:
        return await self._dialogue_template_repository.get_templates(
            offset=(page - 1) * DIALOGUE_TEMPLATES_PER_PAGE,
            limit=DIALOGUE_TEMPLATES_PER_PAGE,
        )

    async def get_template(self, template_id: int) -> DialogueTemplateReadDTO:
        template = await self._dialogue_template_repository.get_template(template_id)
        if template is None:
            raise DialogueTemplateNotFoundError
        return template

    async def create_dialogue_from_template(self, user_id: UUID, project_id: int, template_id: int):
        project = await self._project_service.get_project_with_dialogues(user_id=user_id, project_id=project_id)

        active_subscription = await self._subscription_service.get_active_subscription(user_id)
        max_dialogues = MAX_DIALOGUES_WITH_PRO_PLAN if active_subscription else MAX_DIALOGUES_WITH_FREE_PLAN

        if len(project.dialogues) >= max_dialogues:
            raise DialoguesLimitExceededError

        _ = await self.get_template(template_id)

        await self._dialogue_template_repository.create_dialogue_from_template(
            project_id=project_id,
            template_id=template_id,
        )
