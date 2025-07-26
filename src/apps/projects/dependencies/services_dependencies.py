from typing import Annotated

from fastapi import Depends

from src.apps.projects.services import ProjectService

ProjectServiceDI = Annotated[ProjectService, Depends(ProjectService)]
