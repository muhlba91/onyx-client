"""Onyx Client URL helper."""

import aiohttp

from typing import Optional, Any

from ..configuration.configuration import Configuration
from ..utils.const import API_URL, API_HEADERS, API_VERSION
from ..utils.response import check


class UrlHelper:
    """URL helper for performing requests against the HELLA.ONYX API."""

    def __init__(self, config: Configuration, client_session: aiohttp.ClientSession):
        """Initialize the helper.

        config: the ONYX configuration
        client_session: the aiohttp client session to use"""
        self.config = config
        self.client_session = client_session

    @property
    def _headers(self) -> dict:
        """Get all common headers."""
        return {"Authorization": f"Bearer {self.config.access_token}", **API_HEADERS}

    def _base_url(self, with_api: bool = True) -> str:
        """Get the API base URL for this ONYX.CENTER.

        with_api: append the API version to the URL"""
        api = f"{API_URL}/box/{self.config.fingerprint}/api"
        if with_api:
            api = f"{api}/{API_VERSION}"
        return api

    def _url(self, path: str = "", with_api: bool = True) -> str:
        """Get the request URL.

        path: the URL path
        with_api: append the API version to the URL"""
        return f"{self._base_url(with_api=with_api)}{path}"

    async def perform_get_request(
        self, path: str, with_api: bool = True
    ) -> Optional[Any]:
        """Perform a GET request.

        path: the URL path
        with_api: append the API version to the URL"""
        async with self.client_session.get(
            self._url(path, with_api=with_api), headers=self._headers
        ) as response:
            if not check(response):
                return None
            return await response.json()

    async def perform_delete_request(self, path: str) -> Optional[Any]:
        """Perform a DELETE request.

        path: the URL path"""
        async with self.client_session.delete(
            self._url(path), headers=self._headers
        ) as response:
            if not check(response):
                return None
            return await response.json()

    async def perform_post_request(self, path: str, data: dict) -> Optional[Any]:
        """Perform a POST request.

        path: the URL path
        data: the data to POST to the API"""
        async with self.client_session.post(
            self._url(path), json=data, headers=self._headers
        ) as response:
            if not check(response):
                return None
            return await response.json()

    async def start_stream(self, path: str):
        """Start a stream and returns the value if it's not empty.

        path: the URL path"""
        async with self.client_session.get(
            self._url(path),
            headers=self._headers,
            timeout=aiohttp.ClientTimeout(
                total=0, connect=0, sock_connect=0, sock_read=0
            ),
        ) as response:
            if not check(response):
                yield None
                return
            async for message in response.content:
                cleaned_message = str(message.strip(), "UTF-8").strip()
                if len(cleaned_message) > 0:
                    yield cleaned_message
