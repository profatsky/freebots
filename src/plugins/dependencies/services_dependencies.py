from typing import Annotated

from fastapi import Depends

from src.plugins.services import PluginService

PluginServiceDI = Annotated[PluginService, Depends(PluginService)]
