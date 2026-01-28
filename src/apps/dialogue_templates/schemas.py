import datetime

from pydantic import BaseModel


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
