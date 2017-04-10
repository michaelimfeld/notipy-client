"""
`notipy` - User-Notification-Framework client

Provides the notipy client.

:copyright: (c) by Michael Imfeld
:license: MIT, see LICENSE for details
"""
import json
from pathlib import Path

import requests
from jinja2 import Template

from .errors import TemplateNameNotSetError, TemplateDirNotSetError
from .errors import NotificationSendError


class Notipy:
    """
    Provides functions to interact with the notipy
    server.
    """
    API_VERSION = "v1"

    def __init__(self, server_address, server_port, template_dir=None):
        self.__server_address = server_address
        self.__server_port = server_port
        self.__template_dir = template_dir

    def render_template(self, template_name, **kwargs):
        """
        Renders a template with given keyword
        arguments.

        Args:
            template_name (str): The template's name.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            TemplateNameNotSetError: If no template name was set previously.
            TemplateDirNotSetError: If no template dir was set previously.
            FileNotFoundError: If the template file could not be found.
            TypeError: If template_dir has wrong type.

        Returns:
            str: The rendered template.
        """
        if not self.__template_dir:
            raise TemplateDirNotSetError("template_dir must be set"
                                         " in order to use templating")

        if not isinstance(self.__template_dir, Path):
            raise TypeError("template_dir must be pathlib.Path")

        if not template_name:
            raise TemplateNameNotSetError()

        template_file = (self.__template_dir /
                         template_name).with_suffix(".tmpl")

        if not template_file.exists():
            raise FileNotFoundError(template_file)

        with template_file.open(encoding="utf-8") as _file:
            template_text = _file.read()
            template = Template(template_text)
            return template.render(**kwargs)

    def send(self, backend, recipient, message):
        """
        Sends a notification with the given message
        over the given backend to the given recipient.

        Args:
            backend (notipy.BackendType): The backend to be used.
            recipient (str): The recipient of the message.
            message (str): The message to be sent.

        Raises:
            NotificationSendError: If the notification could not be
                sent successfully
        """
        data = {"backend": backend.value,
                "recipient": recipient,
                "message": message}
        self.send_notification_request(data)

    def send_templated(self, backend, recipient, template_name, **kwargs):
        """
        Sends a notification over the given backend to the given recipient
        using the given template and key word arguments.

        Args:
            backend (notipy.BackendType): The backend to be used.
            recipient (str): The recipient of the message.
            template_name (str): The template's name to be used.

        Raises:
            NotificationSendError: If the notification could not be
                sent successfully
        """
        message_content = self.render_template(template_name, **kwargs)
        data = {"backend": backend.value,
                "recipient": recipient,
                "message": message_content}
        self.send_notification_request(data)

    def send_notification_request(self, data):
        """
        Sends a notification post request to the api server
        with given payload data.

        Args:
            data (dict): The payload to be sent.
        """
        url = "http://{}:{}/api/{}/notifications/send".format(
            self.__server_address, self.__server_port, self.API_VERSION)
        headers = {"content-type": "application/json"}

        response = requests.post(url, data=json.dumps(data), headers=headers)
        self.parse_response(response)

    @staticmethod
    def parse_response(response):
        """
        Parses the given requests response.

        Args:
            response: The response object.

        Raises:
            NotificationSendError: If the notification could not be
                sent successfully
        """
        response_data = response.json()
        if response.status_code != 200:
            raise NotificationSendError("Notification could not be sent: '{}'"
                                        .format(response_data.get("message")))
