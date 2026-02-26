from enum import StrEnum


class LLMChatMemberRole(StrEnum):
    USER = 'user'
    ASSISTANT = 'assistant'
    SYSTEM = 'system'
