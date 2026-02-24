from dataclasses import dataclass

from src.apps.blocks.dto.base import BlockReadDTO
from src.apps.dialogues.dto import DialogueReadDTO
from src.apps.plugins.dto import PluginReadDTO
from src.apps.projects.dto import ProjectReadDTO


@dataclass(frozen=True)
class DialogueWithBlocksReadDTO(DialogueReadDTO):
    blocks: list[BlockReadDTO]


@dataclass(frozen=True)
class ProjectCodeGenReadDTO(ProjectReadDTO):
    dialogues: list[DialogueWithBlocksReadDTO]
    plugins: list[PluginReadDTO]
