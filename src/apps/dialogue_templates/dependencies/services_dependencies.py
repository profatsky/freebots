from typing import Annotated

from fastapi import Depends

from src.apps.dialogue_templates.services import DialogueTemplateService

DialogueTemplateServiceDI = Annotated[DialogueTemplateService, Depends(DialogueTemplateService)]
