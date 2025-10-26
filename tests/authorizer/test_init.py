"""Tests for __init__."""

import aiohttp
import pytest

from unittest.mock import patch
from aioresponses import aioresponses

from onyx_client.authorizer import exchange_code, authorize, _api_url
from onyx_client.configuration.configuration import Configuration
from onyx_client.utils.const import API_URL


@patch("aiohttp.ClientSession")
@patch("onyx_client.authorizer.authorize")
@patch("onyx_client.client.OnyxClient.verify")
@pytest.mark.asyncio
async def test_exchange_code(mock_verify, mock_authorize, mock_session):
    config = await exchange_code("code", mock_session)
    assert config is not None
    assert mock_authorize.called
    assert mock_verify.called


@patch("aiohttp.ClientSession")
@patch("onyx_client.authorizer.authorize")
@patch("onyx_client.client.OnyxClient.verify")
@pytest.mark.asyncio
async def test_exchange_code_failed(mock_verify, mock_authorize, mock_session):
    mock_verify.return_value = False
    config = await exchange_code("code", mock_session)
    assert config is None
    assert mock_authorize.called
    assert mock_verify.called


@pytest.mark.asyncio
async def test_authorize():
    session = aiohttp.ClientSession()
    with aioresponses() as mock_response:
        mock_response.post(
            f"{API_URL}/authorize",
            status=200,
            payload={
                "fingerprint": "finger",
                "token": "token",
            },
        )
        config = await authorize("code", session)
        assert isinstance(config, Configuration)
        assert config.fingerprint == "finger"
        assert config.access_token == "token"
        assert config.local_address is None
    await session.close()


@pytest.mark.asyncio
async def test_authorize_with_local_address():
    session = aiohttp.ClientSession()
    with aioresponses() as mock_response:
        mock_response.post(
            "https://localhost/api/v3/authorize",
            status=200,
            payload={
                "fingerprint": "finger",
                "token": "token",
            },
        )
        config = await authorize("code", session, local_address="localhost")
        assert isinstance(config, Configuration)
        assert config.fingerprint == "finger"
        assert config.access_token == "token"
        assert config.local_address == "localhost"
    await session.close()


@pytest.mark.asyncio
async def test_authorize_error():
    session = aiohttp.ClientSession()
    with aioresponses() as mock_response:
        mock_response.post(f"{API_URL}/authorize", status=401)
        auth = await authorize("code", session)
        assert auth is None
    await session.close()


def test_api_url():
    assert _api_url() == API_URL


def test_api_url_with_local_address():
    assert _api_url("localhost") == "https://localhost/api/v3"
    assert _api_url("127.0.0.1") == "https://127.0.0.1/api/v3"
