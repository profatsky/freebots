from typing import Annotated

from fastapi import Depends

from src.apps.dialogues.services import DialogueService

DialogueServiceDI = Annotated[DialogueService, Depends(DialogueService)]
