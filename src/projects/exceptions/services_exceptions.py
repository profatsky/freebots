class ProjectNotFoundError(Exception):
    pass


class NoPermissionForProjectError(Exception):
    pass


class ProjectsLimitExceededError(Exception):
    pass
