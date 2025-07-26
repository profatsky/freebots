from typing import Annotated

from fastapi import Depends

from src.apps.dialogue_templates.repositories import DialogueTemplateRepository

DialogueTemplateRepositoryDI = Annotated[DialogueTemplateRepository, Depends(DialogueTemplateRepository)]
