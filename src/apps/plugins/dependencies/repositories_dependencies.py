from typing import Annotated

from fastapi import Depends

from src.apps.plugins.repositories import PluginRepository

PluginRepositoryDI = Annotated[PluginRepository, Depends(PluginRepository)]
