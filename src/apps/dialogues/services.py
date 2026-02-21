from uuid import UUID

from src.apps.dialogues.dependencies.repositories_dependencies import DialogueRepositoryDI
from src.apps.dialogues.dto import DialogueCreateDTO, DialogueReadDTO, DialogueTriggerUpdateDTO
from src.apps.dialogues.errors import DialogueNotFoundError, DialoguesLimitExceededError
from src.apps.projects.dependencies.services_dependencies import ProjectServiceDI
from src.apps.subscriptions.dependencies.services_dependencies import SubscriptionServiceDI
from src.core.config import MEDIA_DIR
from src.core.consts import MAX_DIALOGUES_WITH_FREE_PLAN, MAX_DIALOGUES_WITH_PRO_PLAN


class DialogueService:
    def __init__(
        self,
        dialogue_repository: DialogueRepositoryDI,
        project_service: ProjectServiceDI,
        subscription_service: SubscriptionServiceDI,
    ):
        self._dialogue_repository = dialogue_repository
        self._project_service = project_service
        self._subscription_service = subscription_service

    async def create_dialogue(self, user_id: UUID, dialogue: DialogueCreateDTO) -> DialogueReadDTO:
        project = await self._project_service.get_project_with_dialogues(
            user_id=user_id,
            project_id=dialogue.project_id,
        )

        active_subscription = await self._subscription_service.get_active_subscription(user_id)
        max_dialogues = MAX_DIALOGUES_WITH_PRO_PLAN if active_subscription else MAX_DIALOGUES_WITH_FREE_PLAN

        if len(project.dialogues) >= max_dialogues:
            raise DialoguesLimitExceededError

        return await self._dialogue_repository.create_dialogue(dialogue)

    async def update_dialogue_trigger(
        self,
        user_id: UUID,
        project_id: int,
        dialogue_id: int,
        trigger: DialogueTriggerUpdateDTO,
    ) -> DialogueReadDTO:
        _ = await self.get_dialogue(user_id=user_id, project_id=project_id, dialogue_id=dialogue_id)
        return await self._dialogue_repository.update_dialogue_trigger(dialogue_id=dialogue_id, trigger=trigger)

    async def get_dialogue(self, user_id: UUID, project_id: int, dialogue_id: int) -> DialogueReadDTO:
        project = await self._project_service.get_project(user_id=user_id, project_id=project_id)
        dialogue = await self._dialogue_repository.get_dialogue(dialogue_id=dialogue_id)
        if dialogue is None or dialogue.project_id != project.project_id:
            raise DialogueNotFoundError
        return dialogue

    async def delete_dialogue(self, user_id: UUID, project_id: int, dialogue_id: int):
        _ = await self.get_dialogue(user_id=user_id, project_id=project_id, dialogue_id=dialogue_id)

        media_dir = MEDIA_DIR / 'users' / str(user_id) / 'projects' / str(project_id) / 'dialogues' / str(dialogue_id)
        if media_dir.exists():
            media_dir.rmdir()

        await self._dialogue_repository.delete_dialogue(dialogue_id)

    # async def raise_error_if_not_exists(self, user_id: UUID, project_id: int, dialogue_id: int):
    #     await self._project_service.raise_error_if_not_exists(user_id, project_id)
    #     if not await self._dialogue_repository.exists_by_id(project_id, dialogue_id):
    #         raise DialogueNotFoundError
