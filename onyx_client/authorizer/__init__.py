"""Onyx Client authorizer."""
import logging
import aiohttp

from typing import Optional

from ..client import OnyxClient
from ..configuration.configuration import Configuration
from ..utils.const import API_URL, API_HEADERS
from ..utils.response import check

_LOGGER = logging.getLogger(__name__)


async def exchange_code(
    code: str, client_session: aiohttp.ClientSession = None
) -> Optional[Configuration]:
    """Exchange an API code for an access token and fingerprint.

    code: the access code
    client_session: the aiohttp client session to use"""
    session = client_session if client_session is not None else aiohttp.ClientSession()
    config = await authorize(code, session)
    if config is not None and await OnyxClient(config, session).verify():
        return config
    return None


async def authorize(
    code: str, client_session: aiohttp.ClientSession
) -> Optional[Configuration]:
    """Authorize the client using an API code.

    code: the access code
    client_session: the aiohttp client session to use"""
    async with client_session.post(
        f"{API_URL}/authorize",
        json={"code": code},
        headers=API_HEADERS,
    ) as response:
        if not check(response):
            _LOGGER.error("Could not authorize client for ONYX API.")
            return None
        data = await response.json()
        return Configuration(data.get("fingerprint", None), data.get("token", None))
