from typing import Annotated

from fastapi import Depends

from src.dialogues.repositories import DialogueRepository

DialogueRepositoryDI = Annotated[DialogueRepository, Depends(DialogueRepository)]
