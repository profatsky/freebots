from typing import Annotated

from fastapi import Depends

from src.dialogues.services import DialogueService

DialogueServiceDI = Annotated[DialogueService, Depends(DialogueService)]
