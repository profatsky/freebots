import os
import shutil
from uuid import UUID

from src.apps.dialogues.dependencies.repositories_dependencies import DialogueRepositoryDI
from src.apps.dialogues.schemas import (
    DialogueCreateSchema,
    DialogueReadSchema,
    TriggerUpdateSchema,
)
from src.apps.dialogues.exceptions.services_exceptions import DialogueNotFoundError, DialoguesLimitExceededError
from src.apps.projects.dependencies.services_dependencies import ProjectServiceDI
from src.apps.subscriptions.dependencies.services_dependencies import SubscriptionServiceDI
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

    async def create_dialogue(
        self,
        user_id: UUID,
        project_id: int,
        dialogue_data: DialogueCreateSchema,
    ) -> DialogueReadSchema:
        project = await self._project_service.get_project(user_id, project_id)

        active_subscription = await self._subscription_service.get_active_subscription(user_id)
        max_dialogues = MAX_DIALOGUES_WITH_PRO_PLAN if active_subscription else MAX_DIALOGUES_WITH_FREE_PLAN

        if len(project.dialogues) >= max_dialogues:
            raise DialoguesLimitExceededError

        return await self._dialogue_repository.create_dialogue(project_id, dialogue_data)

    async def update_dialogue_trigger(
        self,
        user_id: UUID,
        project_id: int,
        dialogue_id: int,
        trigger: TriggerUpdateSchema,
    ) -> DialogueReadSchema:
        await self._project_service.raise_error_if_not_exists(user_id, project_id)
        dialogue = await self._dialogue_repository.update_dialogue_trigger(dialogue_id, trigger)
        if dialogue is None:
            raise DialogueNotFoundError

        return dialogue

    # TODO: refactor!
    async def get_dialogue(
        self,
        user_id: UUID,
        project_id: int,
        dialogue_id: int,
    ) -> DialogueReadSchema:
        project = await self._project_service.get_project(
            user_id=user_id,
            project_id=project_id,
        )

        dialogue_with_specified_id = None
        for dialogue in project.dialogues:
            if dialogue.dialogue_id == dialogue_id:
                dialogue_with_specified_id = dialogue
                break

        if dialogue_with_specified_id is None:
            raise DialogueNotFoundError

        return dialogue_with_specified_id

    async def delete_dialogue(
        self,
        user_id: UUID,
        project_id: int,
        dialogue_id: int,
    ):
        await self.raise_error_if_not_exists(user_id, project_id, dialogue_id)

        media_dir_path = os.path.join(
            'src', 'media', 'users', str(user_id), 'projects', str(project_id), 'dialogues', str(dialogue_id)
        )
        if os.path.exists(media_dir_path):
            shutil.rmtree(media_dir_path)

        await self._dialogue_repository.delete_dialogue(dialogue_id)

    async def raise_error_if_not_exists(self, user_id: UUID, project_id: int, dialogue_id: int):
        await self._project_service.raise_error_if_not_exists(user_id, project_id)
        if not await self._dialogue_repository.exists_by_id(project_id, dialogue_id):
            raise DialogueNotFoundError
