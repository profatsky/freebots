from typing import Annotated

from fastapi import Depends

from src.projects.services import ProjectService

ProjectServiceDI = Annotated[ProjectService, Depends(ProjectService)]
