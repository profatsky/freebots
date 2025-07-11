from typing import Annotated

from fastapi import Depends

from src.plugins.repositories import PluginRepository

PluginRepositoryDI = Annotated[PluginRepository, Depends(PluginRepository)]
