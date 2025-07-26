from typing import Annotated

from fastapi import Depends

from src.apps.dialogues.repositories import DialogueRepository

DialogueRepositoryDI = Annotated[DialogueRepository, Depends(DialogueRepository)]
