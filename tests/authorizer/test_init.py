"""Tests for __init__."""

from unittest.mock import patch

import aiohttp
import pytest
from aioresponses import aioresponses

from onyx_client.authorizer import _api_url, authorize, exchange_code
from onyx_client.configuration.configuration import Configuration
from onyx_client.utils.const import API_URL


@patch("aiohttp.ClientSession")
@patch("onyx_client.authorizer.authorize")
@patch("onyx_client.client.OnyxClient.__init__", return_value=None)
@patch("onyx_client.client.OnyxClient.verify")
@pytest.mark.asyncio
async def test_exchange_code(mock_verify, mock_init, mock_authorize, mock_session):
    mock_conf = Configuration("finger", "token")
    mock_authorize.return_value = mock_conf
    mock_verify.return_value = True

    config = await exchange_code("code", mock_session, local_address="1.2.3.4")
    assert config == mock_conf
    mock_authorize.assert_called_once_with(
        "code", mock_session, local_address="1.2.3.4"
    )
    assert mock_verify.called
    assert mock_verify.call_count == 1
    mock_init.assert_called_once_with(mock_conf, mock_session)


@patch("onyx_client.authorizer.authorize")
@patch("onyx_client.client.OnyxClient.verify")
@pytest.mark.asyncio
async def test_exchange_code_creates_session_if_none(mock_verify, mock_authorize):
    mock_conf = Configuration("finger", "token")
    mock_authorize.return_value = mock_conf
    mock_verify.return_value = True

    with patch("aiohttp.ClientSession") as mock_cls:
        session_instance = mock_cls.return_value
        config = await exchange_code("code", None)
        assert config == mock_conf
        mock_authorize.assert_called_once_with(
            "code", session_instance, local_address=None
        )


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
    with (
        patch.object(session, "post", wraps=session.post) as mock_post,
        aioresponses() as mock_response,
    ):
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
        mock_post.assert_called_once_with(
            f"{API_URL}/authorize",
            json={"code": "code"},
            headers={"Content-Type": "application/json"},
            ssl=True,
        )
    await session.close()


@pytest.mark.asyncio
async def test_authorize_with_local_address():
    session = aiohttp.ClientSession()
    with (
        patch.object(session, "post", wraps=session.post) as mock_post,
        aioresponses() as mock_response,
    ):
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
        mock_post.assert_called_once_with(
            "https://localhost/api/v3/authorize",
            json={"code": "code"},
            headers={"Content-Type": "application/json"},
            ssl=False,
        )
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
