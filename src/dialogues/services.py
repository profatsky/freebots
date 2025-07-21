import os
import shutil

from src.dialogues.dependencies.repositories_dependencies import DialogueRepositoryDI
from src.dialogues.schemas import (
    DialogueCreateSchema,
    DialogueReadSchema,
    TriggerUpdateSchema,
)
from src.dialogues.exceptions.services_exceptions import DialogueNotFoundError, DialoguesLimitExceededError
from src.projects.dependencies.services_dependencies import ProjectServiceDI


class DialogueService:
    def __init__(
        self,
        dialogue_repository: DialogueRepositoryDI,
        project_service: ProjectServiceDI,
    ):
        self._dialogue_repository = dialogue_repository
        self._project_service = project_service

    async def create_dialogue(
        self,
        user_id: int,
        project_id: int,
        dialogue_data: DialogueCreateSchema,
    ) -> DialogueReadSchema:
        project = await self._project_service.get_project(
            user_id=user_id,
            project_id=project_id,
        )
        if len(project.dialogues) >= 10:
            raise DialoguesLimitExceededError

        return await self._dialogue_repository.create_dialogue(
            project_id=project_id,
            dialogue_data=dialogue_data,
        )

    async def update_dialogue_trigger(
        self,
        user_id: int,
        project_id: int,
        dialogue_id: int,
        trigger: TriggerUpdateSchema,
    ) -> DialogueReadSchema:
        _ = await self._project_service.get_project(
            user_id=user_id,
            project_id=project_id,
        )

        dialogue = await self._dialogue_repository.update_dialogue_trigger(
            dialogue_id=dialogue_id,
            trigger=trigger,
        )
        if dialogue is None:
            raise DialogueNotFoundError

        return dialogue

    async def get_dialogue(
        self,
        user_id: int,
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
        user_id: int,
        project_id: int,
        dialogue_id: int,
    ):
        _ = await self.get_dialogue(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
        )

        media_dir_path = os.path.join(
            'src', 'media', 'users', str(user_id), 'projects', str(project_id), 'dialogues', str(dialogue_id)
        )
        if os.path.exists(media_dir_path):
            shutil.rmtree(media_dir_path)

        await self._dialogue_repository.delete_dialogue(dialogue_id)
