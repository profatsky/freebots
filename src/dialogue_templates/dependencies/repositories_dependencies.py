from typing import Annotated

from fastapi import Depends

from src.dialogue_templates.repositories import DialogueTemplateRepository

DialogueTemplateRepositoryDI = Annotated[DialogueTemplateRepository, Depends(DialogueTemplateRepository)]
