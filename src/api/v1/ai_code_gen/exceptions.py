from fastapi import HTTPException, status


class AICodeGenSessionNotFoundHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='AI code gen session not found',
        )


class AICodeGenNoPermissionHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='No permission for AI code gen session',
        )


class AICodeGenPromptTooLongHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Prompt is too long',
        )


class AICodeGenMessagesLimitExceededHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Messages limit exceeded for this session',
        )


class AICodeGenInvalidResponseHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail='Invalid response from LLM',
        )


class AICodeGenResponseTooLongHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Generated response is too long',
        )


class AICodeGenNoAssistantMessageHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No generated code to download',
        )
