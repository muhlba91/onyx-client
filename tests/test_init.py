"""Tests for __init__."""
from unittest.mock import patch

from onyx_client import Configuration, create_client


@patch("aiohttp.ClientSession")
def test_create_client(mock_session):
    client = create_client(
        fingerprint="finger", access_token="token", client_session=mock_session
    )
    assert client.client_session == mock_session
    assert client.config.fingerprint == "finger"
    assert client.config.access_token == "token"


@patch("aiohttp.ClientSession")
def test_create_client_with_config(mock_session):
    client = create_client(
        config=Configuration("finger", "token"), client_session=mock_session
    )
    assert client.client_session == mock_session
    assert client.config is not None
    assert client.config.fingerprint == "finger"
    assert client.config.access_token == "token"


@patch("aiohttp.ClientSession")
def test_create_client_without_session(mock_session):
    client = create_client(fingerprint="finger", access_token="token")
    assert client.client_session is not None
    assert client.config.fingerprint == "finger"
    assert client.config.access_token == "token"
