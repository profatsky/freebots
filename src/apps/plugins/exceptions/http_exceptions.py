from fastapi import HTTPException, status


class PluginNotFoundHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Plugin does not exist',
        )


class PluginAlreadyInProjectHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='The specified plugin is already in the project',
        )


class PluginIsNotInProjectHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='The specified plugin is not in the project',
        )
