from src.apps.dialogue_templates.dependencies.repositories_dependencies import DialogueTemplateRepositoryDI
from src.apps.dialogue_templates.exceptions.services_exceptions import DialogueTemplateNotFoundError
from src.apps.dialogue_templates.schemas import DialogueTemplateReadSchema
from src.apps.projects.dependencies.services_dependencies import ProjectServiceDI

DIALOGUE_TEMPLATES_PER_PAGE = 9


class DialogueTemplateService:
    def __init__(
        self,
        dialogue_template_repository: DialogueTemplateRepositoryDI,
        project_service: ProjectServiceDI,
    ):
        self._dialogue_template_repository = dialogue_template_repository
        self._project_service = project_service

    async def get_templates(
        self,
        page: int,
    ) -> list[DialogueTemplateReadSchema]:
        return await self._dialogue_template_repository.get_templates(
            offset=(page - 1) * DIALOGUE_TEMPLATES_PER_PAGE,
            limit=DIALOGUE_TEMPLATES_PER_PAGE,
        )

    async def get_template(
        self,
        template_id: int,
    ) -> DialogueTemplateReadSchema:
        template = await self._dialogue_template_repository.get_template(template_id)
        if template is None:
            raise DialogueTemplateNotFoundError
        return template

    async def create_dialogue_from_template(
        self,
        user_id: int,
        project_id: int,
        template_id: int,
    ):
        _ = await self._project_service.get_project(
            user_id=user_id,
            project_id=project_id,
        )

        _ = await self.get_template(template_id)

        await self._dialogue_template_repository.create_dialogue_from_template(
            project_id=project_id,
            template_id=template_id,
        )
