"""HTTP Client for Hella's ONYX.CENTER API."""
import aiohttp

from onyx_client.client import OnyxClient
from onyx_client.configuration.configuration import Configuration


def create_client(
    config: Configuration = None,
    fingerprint: str = None,
    access_token: str = None,
    client_session: aiohttp.ClientSession = None,
) -> OnyxClient:
    if config is None:
        config = Configuration(fingerprint, access_token)
    session = client_session if client_session is not None else aiohttp.ClientSession()
    return OnyxClient(config, session)
