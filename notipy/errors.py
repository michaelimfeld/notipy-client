"""
`notipy` - User-Notification-Framework client

Provides a collection of all possible
notipy errors.

:copyright: (c) by Michael Imfeld
:license: MIT, see LICENSE for details
"""


class NotipyError(Exception):
    """
    Represents the base exception for notipy specific
    errors.
    """
    pass


class TemplateNameNotSetError(NotipyError):
    """
    Exception which is raised if no template name
    was set.
    """
    pass


class TemplateDirNotSetError(NotipyError):
    """
    Exception which is raised if no template directory
    was set.
    """
    pass


class ApiError(NotipyError):
    """
    Represents the base exception for rest api specific
    errors.
    """
    pass


class NotificationSendError(ApiError):
    """
    Exception which is raised if the notification
    could not be sent over the api.
    """
    pass
