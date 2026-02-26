from enum import StrEnum


class AICodeGenRole(StrEnum):
    USER = 'user'
    ASSISTANT = 'assistant'
    SYSTEM = 'system'
