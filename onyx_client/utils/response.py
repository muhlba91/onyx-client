"""Onyx Client response utils."""
import logging

import aiohttp

_LOGGER = logging.getLogger(__name__)


def check(response: aiohttp.ClientResponse) -> bool:
    """Check the response for a success HTTP status code.

    Success codes are:
      - 200"""
    if response.status == 200:
        _LOGGER.debug("Received HTTP response from ONYX API: %s", response.status)
        return True
    else:
        _LOGGER.error(
            "Received erroneous HTTP response from ONYX API: %s", response.status
        )
        return False
