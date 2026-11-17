"""Onyx Client URL helper."""

from typing import Any

import aiohttp

from ..configuration.configuration import Configuration
from ..utils.const import (
    API_HEADERS,
    API_URL,
    STREAM_CONNECT_TIMEOUT,
    STREAM_READ_TIMEOUT,
)
from ..utils.response import check
from ..utils.sanitize import strip_credentials


class UrlHelper:
    """URL helper for performing requests against the HELLA.ONYX API."""

    def __init__(self, config: Configuration, client_session: aiohttp.ClientSession):
        """Initialize the helper.

        config: the ONYX configuration
        client_session: the aiohttp client session to use"""
        self.config = config
        self.client_session = client_session
        self._stream_response = None

    @property
    def _headers(self) -> dict:
        """Get all common headers."""
        return {"Authorization": f"Bearer {self.config.access_token}", **API_HEADERS}

    def _base_url(self, with_api: bool = True) -> str:
        """Get the API base URL for this ONYX.CENTER.

        with_api: append the API version to the URL"""
        api = f"{API_URL}/box/{self.config.fingerprint}/api"
        if self.config.local_address:
            api = f"https://{self.config.local_address}/api"
        if with_api:
            api = f"{api}/{self.config.api_version}"
        return api

    def _url(self, path: str = "", with_api: bool = True) -> str:
        """Get the request URL.

        path: the URL path
        with_api: append the API version to the URL"""
        return f"{self._base_url(with_api=with_api)}{path}"

    async def perform_get_request(self, path: str, with_api: bool = True) -> Any | None:
        """Perform a GET request.

        path: the URL path
        with_api: append the API version to the URL"""
        try:
            async with self.client_session.get(
                self._url(path, with_api=with_api),
                headers=self._headers,
                ssl=not self.config.is_local,
            ) as response:
                if not check(response):
                    return None
                return await response.json()
        except aiohttp.ClientResponseError as ex:
            strip_credentials(ex)
            raise

    async def perform_delete_request(self, path: str) -> Any | None:
        """Perform a DELETE request.

        path: the URL path"""
        try:
            async with self.client_session.delete(
                self._url(path), headers=self._headers, ssl=not self.config.is_local
            ) as response:
                if not check(response):
                    return None
                return await response.json()
        except aiohttp.ClientResponseError as ex:
            strip_credentials(ex)
            raise

    async def perform_post_request(
        self, path: str, data: dict | None = None
    ) -> Any | None:
        """Perform a POST request.

        path: the URL path
        data: the data to POST to the API (default: no body)"""
        try:
            async with self.client_session.post(
                self._url(path),
                json=data,
                headers=self._headers,
                ssl=not self.config.is_local,
            ) as response:
                if not check(response):
                    return None
                return await response.json()
        except aiohttp.ClientResponseError as ex:
            strip_credentials(ex)
            raise

    async def perform_status_request(self, method: str, path: str) -> int:
        """Perform a request and return only its HTTP status code.

        method: the HTTP method
        path: the URL path"""
        async with self.client_session.request(
            method, self._url(path), headers=self._headers, ssl=not self.config.is_local
        ) as response:
            return response.status

    async def start_stream(self, path: str):
        """Start a stream and yield its lines without line endings.

        Lines are split without a length limit (a snapshot is a single line).
        Raises aiohttp.ClientResponseError on an erroneous HTTP response and
        aiohttp.ServerTimeoutError if no data arrives within the read timeout.

        path: the URL path"""
        try:
            async with self.client_session.get(
                self._url(path),
                headers=self._headers,
                timeout=aiohttp.ClientTimeout(
                    total=None,
                    sock_connect=STREAM_CONNECT_TIMEOUT,
                    sock_read=STREAM_READ_TIMEOUT,
                ),
                ssl=not self.config.is_local,
            ) as response:
                response.raise_for_status()
                self._stream_response = response
                buffer = b""
                try:
                    async for chunk in response.content.iter_any():
                        *lines, buffer = (buffer + chunk).split(b"\n")
                        for line in lines:
                            yield _decode(line)
                    if buffer:
                        yield _decode(buffer)
                finally:
                    self._stream_response = None
        except aiohttp.ClientResponseError as ex:
            strip_credentials(ex)
            raise

    def close_stream(self):
        """Close the running stream, if any."""
        if self._stream_response is not None:
            self._stream_response.close()


def _decode(line: bytes) -> str:
    """Decode a stream line without its line ending.

    line: the raw line"""
    return line.decode("utf-8", errors="replace").rstrip("\r")
