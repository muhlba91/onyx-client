"""Onyx Client response utils."""

import logging

import aiohttp

_LOGGER = logging.getLogger(__name__)


def check(response: aiohttp.ClientResponse) -> bool:
    """Check the response for a success HTTP status code.

    Success codes are:
      - 200

    response: the response to check"""
    if response.status == 200:
        # pragma: no mutate start
        _LOGGER.debug("Received HTTP response from ONYX API: %s", response.status)
        # pragma: no mutate end
        return True
    else:
        # pragma: no mutate start
        _LOGGER.error(
            "Received erroneous HTTP response from ONYX API: %s", response.status
        )
        # pragma: no mutate end
        return False
