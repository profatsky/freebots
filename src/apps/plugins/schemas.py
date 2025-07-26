import datetime

from pydantic import BaseModel


class PluginReadSchema(BaseModel):
    plugin_id: int
    name: str
    summary: str
    description: str
    image_path: str
    created_at: datetime.datetime
    handlers_file_path: str
    db_funcs_file_path: str

    model_config = {
        'from_attributes': True,
    }


class PluginCreateSchema(BaseModel):
    name: str
    summary: str
    description: str
    image_path: str
    handlers_file_path: str
    db_funcs_file_path: str
