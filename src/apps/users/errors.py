class UserAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class DontHavePermissionError(Exception):
    pass
