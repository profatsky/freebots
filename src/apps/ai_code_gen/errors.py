class AICodeGenSessionNotFoundError(Exception):
    pass


class AICodeGenSessionNoPermissionError(Exception):
    pass


class AICodeGenPromptTooLongError(Exception):
    pass


class AICodeGenMessagesLimitExceededError(Exception):
    pass


class AICodeGenInvalidResponseError(Exception):
    pass


class AICodeGenNoAssistantMessageError(Exception):
    pass
