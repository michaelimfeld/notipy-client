"""
`notipy` - User-Notification-Framework client

Provides test cases for the notipy module.

:copyright: (c) by Michael Imfeld
:license: MIT, see LICENSE for details
"""
import tempfile
from pathlib import Path

from mock import patch, MagicMock
from nose.tools import assert_raises, assert_equal

from notipy.core import Notipy
from notipy.backendtype import BackendType
from notipy.errors import TemplateDirNotSetError
from notipy.errors import TemplateNameNotSetError
from notipy.errors import NotificationSendError


def test_render_template_notmpldir():
    """
    Test render template if not template dir is set
    """
    notifier = Notipy("foo", 1234)
    assert_raises(TemplateDirNotSetError, notifier.render_template, "bar")


def test_render_template_wrngtypdir():
    """
    Test render template if template dir has wrong type
    """
    notifier = Notipy("foo", 1234, template_dir="bar")
    assert_raises(TypeError, notifier.render_template, "bar")


def test_render_template_notmplname():
    """
    Test render template if template name is None
    """
    notifier = Notipy("foo", 1234, template_dir=Path("bar"))
    assert_raises(TemplateNameNotSetError, notifier.render_template, None)


def test_render_template_nofile():
    """
    Test render template if template file does not exist
    """
    notifier = Notipy("foo", 1234, template_dir=Path("/foobarfoo"))
    assert_raises(FileNotFoundError, notifier.render_template, "nonexistent")


def test_render_template():
    """
    Test render template
    """
    template_file_content = """Hello {{ name }}."""
    tmp_file = tempfile.TemporaryFile(suffix=".tmpl")

    with Path(str(tmp_file.name) + ".tmpl").open(mode="w+") as _file:
        _file.write(template_file_content)

    notifier = Notipy("foo", 1234, template_dir=Path("."))
    res = notifier.render_template(str(tmp_file.name), name="Jon")
    assert_equal(res, "Hello Jon.")

    tmp_file.close()


def test_send():
    """
    Test sending of a message
    """
    with patch.object(Notipy, "send_notification_request") as mock:
        notifier = Notipy("foo", 1234)
        backend = BackendType.TELEGRAM

        notifier.send(backend, "foouser", "hello")
        mock.assert_called_with({"backend": backend.value,
                                 "recipient": "foouser",
                                 "message": "hello"})


def test_send_fail():
    """
    Test sending of a message when sending fails
    """
    with patch.object(Notipy, "send_notification_request") as mock:
        mock.side_effect = NotificationSendError()

        notifier = Notipy("foo", 1234)
        backend = BackendType.TELEGRAM

        assert_raises(NotificationSendError, notifier.send, backend, "foouser",
                      "hello")


def test_send_templated():
    """
    Test sending of a templated message
    """
    with patch.object(Notipy, "send_notification_request") as mock, \
            patch.object(Notipy, "render_template") as render_mock:

        render_mock.return_value = "foobar"
        notifier = Notipy("foo", 1234)
        backend = BackendType.TELEGRAM

        notifier.send_templated(backend, "foouser", "templatename")
        mock.assert_called_with({"backend": backend.value,
                                 "recipient": "foouser",
                                 "message": "foobar"})


def test_send_templated_fail():
    """
    Test sending of a templated message when sending fails
    """
    with patch.object(Notipy, "send_notification_request") as mock, \
            patch.object(Notipy, "render_template"):
        mock.side_effect = NotificationSendError()

        notifier = Notipy("foo", 1234)
        backend = BackendType.TELEGRAM

        assert_raises(NotificationSendError, notifier.send_templated, backend,
                      "foouser", "templatename")


def test_send_notification_request():
    """
    Test sending of a notification request
    """
    with patch.object(Notipy, "parse_response"), \
            patch("requests.post") as post_mock:
        notifier = Notipy("foo", 1234)
        notifier.send_notification_request({"foo": "bar"})
        post_mock.assert_called_with(
            "http://foo:1234/api/v1/notifications/send",
            data='{"foo": "bar"}',
            headers={"content-type": "application/json"})


def test_parse_response():
    """
    Test parsing of a response
    """
    response = MagicMock()
    response.status_code = 200
    response.json = MagicMock()

    Notipy.parse_response(response)


def test_parse_response_fail():
    """
    Test parsing of an error response
    """
    response = MagicMock()
    response.status_code = 500
    response.json = MagicMock()

    assert_raises(NotificationSendError, Notipy.parse_response, response)
