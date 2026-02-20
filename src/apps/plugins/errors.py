class PluginNotFoundError(Exception):
    pass


class PluginAlreadyInProjectError(Exception):
    pass


class PluginIsNotInProjectError(Exception):
    pass


class PluginsLimitExceededError(Exception):
    pass


class PluginsNotAvailableForFreeUsersError(Exception):
    pass
