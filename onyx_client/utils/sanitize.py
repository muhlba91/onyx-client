"""Onyx Client sanitize utils."""

import json
import logging
import re
from urllib.parse import urlsplit

import aiohttp
from multidict import CIMultiDict, CIMultiDictProxy

from ..exception.invalid_stream_data import InvalidStreamDataException

MASK = "***"

_BEARER = re.compile(r"(?i)\b(bearer)\s+[^\s'\",;)]+")
_AUTHORIZATION = re.compile(
    r"(?i)(['\"]?authorization['\"]?\s*[:=]\s*)(['\"]?)(?!bearer\b)[^\s'\",;)]+"
)
_BOX = re.compile(r"(?<=/box/)[^/]+")


def redact(text: str) -> str:
    """Mask bearer tokens and Authorization header values in a text.

    This is a backstop only: it masks Bearer tokens and Authorization header
    values, nothing else.

    text: the text to sanitize"""
    text = _BEARER.sub(rf"\1 {MASK}", text)
    return _AUTHORIZATION.sub(rf"\1\2{MASK}", text)


def describe_exception(exc: BaseException) -> str:
    """Describe an exception without its repr, which may contain request headers.

    The repr of an aiohttp.ClientResponseError includes the request headers
    and thereby the access token. The description only contains the class
    name and, where it is known to be safe, the HTTP status, reason, host and
    path (without query). The fingerprint in the path is not a credential but
    is masked to keep logs shareable. Connection, payload and JSON errors add
    their (redacted, bounded) text; timeouts only their class name.

    exc: the exception to describe"""
    parts = [type(exc).__name__]
    if isinstance(exc, aiohttp.ClientResponseError):
        parts.append(f"status={exc.status}")
        if exc.message:
            parts.append(f"message={redact(str(exc.message))!r}")
        try:
            url = urlsplit(str(exc.request_info.real_url))
        except (AttributeError, ValueError):
            url = None
        if url is not None and url.hostname:
            parts.append(f"host={url.hostname}")
            parts.append(f"path={_BOX.sub(MASK, url.path)}")
    elif isinstance(
        exc,
        (
            InvalidStreamDataException,
            aiohttp.ClientConnectionError,
            aiohttp.ClientPayloadError,
            json.JSONDecodeError,
        ),
    ) and not isinstance(exc, TimeoutError):
        text = redact(str(exc))[:200]
        if text:
            parts.append(text)
    return " ".join(parts)


def strip_credentials(exc: aiohttp.ClientResponseError) -> None:
    """Remove the request headers, which carry the access token, from the error.

    The exception keeps its type, status, message and URL. Its request info
    is replaced by one without headers and its redirect history is dropped, as
    its responses refer to the original request info.

    exc: the error to strip in place"""
    info = exc.request_info
    if info is not None:
        info = aiohttp.RequestInfo(
            info.url, info.method, CIMultiDictProxy(CIMultiDict()), info.real_url
        )
    exc.request_info = info
    exc.history = ()
    exc.args = (info, ())


class RedactingFilter(logging.Filter):
    """Logging filter masking bearer tokens in the messages of a logger."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Mask credentials in the record.

        record: the log record"""
        try:
            message = record.getMessage()
        except Exception:  # noqa: BLE001 - a malformed call is left to the handler
            return True
        redacted = redact(message)
        if redacted != message:
            record.msg, record.args = redacted, None
        return True


def protect(logger: logging.Logger) -> logging.Logger:
    """Add the RedactingFilter to the logger (once).

    Filters on a logger do not apply to records of its child loggers; protect
    every module logger.

    logger: the logger to protect"""
    if not any(isinstance(f, RedactingFilter) for f in logger.filters):
        logger.addFilter(RedactingFilter())
    return logger
