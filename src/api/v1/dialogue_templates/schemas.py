import datetime
from typing import Self

from pydantic import BaseModel

from src.apps.dialogue_templates.dto import DialogueTemplateReadDTO


class DialogueTemplateReadSchema(BaseModel):
    template_id: int
    name: str
    summary: str
    description: str
    image_path: str
    created_at: datetime.datetime
    readme_file_path: str

    model_config = {
        'from_attributes': True,
    }

    @classmethod
    def from_dto(cls, dto: DialogueTemplateReadDTO) -> Self:
        return cls(
            template_id=dto.template_id,
            name=dto.name,
            summary=dto.summary,
            description=dto.description,
            image_path=dto.image_path,
            created_at=dto.created_at,
            readme_file_path=dto.readme_file_path,
        )
