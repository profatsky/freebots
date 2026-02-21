from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DialogueTemplateReadDTO:
    template_id: int
    name: str
    summary: str
    description: str
    image_path: str
    created_at: datetime
    readme_file_path: str
