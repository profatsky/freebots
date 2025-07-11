from typing import Annotated

from fastapi import Depends

from src.projects.repositories import ProjectRepository

ProjectRepositoryDI = Annotated[ProjectRepository, Depends(ProjectRepository)]
