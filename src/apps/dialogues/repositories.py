from typing import Optional

from sqlalchemy import select, delete, exists
from sqlalchemy.orm import joinedload

from src.core.base_repository import BaseRepository
from src.apps.dialogues.models import TriggerModel, DialogueModel
from src.apps.dialogues.schemas import DialogueCreateSchema, DialogueReadSchema, TriggerUpdateSchema


class DialogueRepository(BaseRepository):
    async def create_dialogue(
        self,
        project_id: int,
        dialogue_data: DialogueCreateSchema,
    ) -> DialogueReadSchema:
        trigger = TriggerModel(**dialogue_data.trigger.model_dump())
        dialogue = DialogueModel(trigger=trigger, project_id=project_id)
        self._session.add(dialogue)
        await self._session.commit()
        return DialogueReadSchema.model_validate(dialogue)

    async def update_dialogue_trigger(
        self,
        dialogue_id: int,
        trigger: TriggerUpdateSchema,
    ) -> Optional[DialogueReadSchema]:
        dialogue = await self._get_dialogue_model_instance(dialogue_id)
        if dialogue is None:
            return

        dialogue.trigger.event_type = trigger.event_type
        dialogue.trigger.value = trigger.value
        await self._session.commit()
        return DialogueReadSchema.model_validate(dialogue)

    async def _get_dialogue_model_instance(self, dialogue_id: int) -> Optional[DialogueModel]:
        dialogue = await self._session.execute(
            select(DialogueModel)
            .options(
                joinedload(DialogueModel.trigger),
            )
            .where(DialogueModel.dialogue_id == dialogue_id)
        )
        return dialogue.scalar()

    async def get_dialogue(self, dialogue_id: int) -> Optional[DialogueReadSchema]:
        dialogue = await self._get_dialogue_model_instance(dialogue_id)
        if dialogue is None:
            return
        return DialogueReadSchema.model_validate(dialogue)

    async def delete_dialogue(self, dialogue_id: int):
        await self._session.execute(delete(DialogueModel).where(DialogueModel.dialogue_id == dialogue_id))
        await self._session.commit()

    async def exists_by_id(self, project_id: int, dialogue_id: int) -> bool:
        return await self._session.scalar(
            select(
                exists().where(
                    DialogueModel.project_id == project_id,
                    DialogueModel.dialogue_id == dialogue_id,
                )
            )
        )
