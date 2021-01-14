"""Onyx Client helpers."""
from typing import Optional

import aiohttp

from onyx_client import OnyxClient
from onyx_client.configuration.configuration import Configuration


async def exchange_code(
    code: str, client_session: aiohttp.ClientSession = None
) -> Optional[Configuration]:
    """Exchange an API code for an access token and fingerprint."""
    session = client_session if client_session is not None else aiohttp.ClientSession()
    config = await OnyxClient.authorize(code, session)
    if await OnyxClient(config, session).verify():
        return config
    return None
