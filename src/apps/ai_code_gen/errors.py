class AICodeGenSessionNotFoundError(Exception):
    pass


class AICodeGenNoPermissionError(Exception):
    pass


class AICodeGenPromptTooLongError(Exception):
    pass


class AICodeGenMessagesLimitExceededError(Exception):
    pass


class AICodeGenInvalidResponseError(Exception):
    pass


class AICodeGenResponseTooLongError(Exception):
    pass


class AICodeGenNoAssistantMessageError(Exception):
    pass
