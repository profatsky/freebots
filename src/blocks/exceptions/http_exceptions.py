from fastapi import HTTPException, status


class BlockNotFoundHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Block does not exist',
        )


class RepeatingBlockSequenceNumberHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Repeating sequence numbers for blocks in the dialogue',
        )


class InvalidBlockTypeHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid block type',
        )
