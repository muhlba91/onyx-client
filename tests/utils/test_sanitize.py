"""Tests for the sanitize utils."""

import json
import logging

import aiohttp
import pytest
from multidict import CIMultiDict, CIMultiDictProxy
from yarl import URL

from onyx_client.exception.invalid_stream_data import InvalidStreamDataException
from onyx_client.utils.sanitize import (
    RedactingFilter,
    describe_exception,
    protect,
    redact,
    strip_credentials,
)

TOKEN = "s3cr3t-t0k3n-value"


def response_error(status=404) -> aiohttp.ClientResponseError:
    url = URL("https://api.hella.link/box/FINGERPRINT/api/v6/events?x=1")
    info = aiohttp.RequestInfo(
        url,
        "GET",
        CIMultiDictProxy(CIMultiDict({"Authorization": f"Bearer {TOKEN}"})),
        url,
    )
    return aiohttp.ClientResponseError(info, (), status=status, message="Not Found")


def test_repr_of_response_error_contains_token():
    # documents why repr() must never be logged
    assert TOKEN in repr(response_error())


def test_describe_response_error():
    description = describe_exception(response_error())
    assert TOKEN not in description
    assert "Authorization" not in description
    assert "FINGERPRINT" not in description
    assert "x=1" not in description
    assert description == (
        "ClientResponseError status=404 message='Not Found' "
        "host=api.hella.link path=/box/***/api/v6/events"
    )


def test_describe_response_error_without_url():
    error = aiohttp.ClientResponseError(None, (), status=500, message="")
    assert describe_exception(error) == "ClientResponseError status=500"


def test_describe_other_exceptions():
    assert describe_exception(TimeoutError(f"Bearer {TOKEN}")) == "TimeoutError"
    assert describe_exception(aiohttp.ServerTimeoutError()) == "ServerTimeoutError"
    assert (
        describe_exception(InvalidStreamDataException("PATCH_BEFORE_SNAPSHOT"))
        == "InvalidStreamDataException PATCH_BEFORE_SNAPSHOT"
    )
    assert TOKEN not in describe_exception(
        InvalidStreamDataException(f"Authorization: Bearer {TOKEN}")
    )


def test_redact():
    assert redact(f"Bearer {TOKEN}") == "Bearer ***"
    assert redact(f"'Authorization': 'Bearer {TOKEN}', 'Host': 'x'") == (
        "'Authorization': 'Bearer ***', 'Host': 'x'"
    )
    assert redact("Authorization: abc123") == "Authorization: ***"
    assert redact("nothing to hide") == "nothing to hide"


def test_filter_masks_message_and_args():
    logger = protect(logging.Logger("t"))  # noqa: LOG001 - unregistered on purpose
    assert protect(logger) is logger
    assert len([f for f in logger.filters if isinstance(f, RedactingFilter)]) == 1
    messages = []
    handler = logging.Handler()
    handler.emit = lambda record: messages.append(record.getMessage())
    logger.addHandler(handler)
    logger.error("failed: %s", f"Bearer {TOKEN}")
    logger.error("fine: %s", 5)
    assert messages == ["failed: Bearer ***", "fine: 5"]


def test_filter_ignores_malformed_log_call():
    record = logging.LogRecord("t", logging.WARNING, "f", 1, "x %d", ("notint",), None)
    assert RedactingFilter().filter(record) is True


def test_strip_credentials():
    error = response_error()
    strip_credentials(error)
    assert TOKEN not in repr(error)
    assert TOKEN not in repr(error.args)
    assert TOKEN not in str(error)
    assert error.status == 404
    assert error.message == "Not Found"
    assert error.request_info.method == "GET"
    assert error.request_info.url == error.request_info.real_url
    assert error.request_info.url.path.endswith("/events")
    assert len(error.request_info.headers) == 0
    assert error.history == ()
    assert "api.hella.link" in str(error)


def test_strip_credentials_without_request_info():
    error = aiohttp.ClientResponseError(None, (), status=500)
    strip_credentials(error)
    assert error.request_info is None
    assert error.args == (None, ())


def test_describe_local_address_has_no_box():
    url = URL("https://192.168.1.2/api/v6/devices")
    info = aiohttp.RequestInfo(url, "GET", CIMultiDictProxy(CIMultiDict()), url)
    error = aiohttp.ClientResponseError(info, (), status=500, message="x")
    assert describe_exception(error) == (
        "ClientResponseError status=500 message='x' "
        "host=192.168.1.2 path=/api/v6/devices"
    )


def test_describe_response_error_with_empty_hostname():
    url = URL("/relative")
    info = aiohttp.RequestInfo(url, "GET", CIMultiDictProxy(CIMultiDict()), url)
    error = aiohttp.ClientResponseError(info, (), status=500)
    assert describe_exception(error) == "ClientResponseError status=500"


@pytest.mark.parametrize(
    "exc",
    [
        aiohttp.ClientConnectorError(
            aiohttp.client_reqrep.ConnectionKey("h", 1, False, True, None, None, None),
            OSError(111, "Connect call failed"),
        ),
        aiohttp.ServerDisconnectedError("Server disconnected"),
        aiohttp.ClientPayloadError("Response payload is not completed"),
        json.JSONDecodeError("Expecting value", "doc", 0),
    ],
    ids=["connector", "disconnected", "payload", "json"],
)
def test_describe_connection_errors_have_detail(exc):
    description = describe_exception(exc)
    assert description.startswith(type(exc).__name__ + " ")
    assert redact(str(exc))[:200] in description


def test_describe_connection_error_is_redacted_and_bounded():
    error = aiohttp.ClientPayloadError(f"Bearer {TOKEN} " + "x" * 500)
    description = describe_exception(error)
    assert TOKEN not in description
    assert len(description) <= len("ClientPayloadError ") + 200


def test_describe_connection_timeout_only_class_name():
    error = aiohttp.ConnectionTimeoutError(f"Bearer {TOKEN}")
    assert describe_exception(error) == "ConnectionTimeoutError"


def test_describe_connection_error_without_text():
    error = aiohttp.ClientConnectionError()
    assert describe_exception(error) == "ClientConnectionError"
