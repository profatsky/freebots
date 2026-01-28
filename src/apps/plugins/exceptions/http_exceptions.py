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
            detail='Указанный плагин уже добавлен в проект',
        )


class PluginIsNotInProjectHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='The specified plugin is not in the project',
        )


class PluginsLimitExceededHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Достигнут лимит по количеству плагинов с тарифом Базовый',
        )


class PluginsNotAvailableForFreeUsersHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Боты с плагинами доступны только с тарифом PRO',
        )
