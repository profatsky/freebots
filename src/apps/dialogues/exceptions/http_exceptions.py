from fastapi import HTTPException, status


class DialoguesLimitExceededHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Достигнут лимит по количеству диалогов с тарифом Базовый',
        )


class DialogueNotFoundHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Dialogue does not exist',
        )


class NoDialoguesInProjectHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='No dialogues in the project',
        )
