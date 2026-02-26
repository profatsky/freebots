from typing import TypedDict

from src.infrastructure.llm.enums import LLMChatMemberRole


class LLMChatMessage(TypedDict):
    role: LLMChatMemberRole
    content: str
