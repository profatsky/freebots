from typing import Annotated

from fastapi import Depends

from src.apps.projects.repositories import ProjectRepository

ProjectRepositoryDI = Annotated[ProjectRepository, Depends(ProjectRepository)]
