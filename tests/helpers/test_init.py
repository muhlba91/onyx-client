"""Tests for __init__."""
from unittest.mock import patch

import pytest

from onyx_client.helpers import exchange_code


@patch("aiohttp.ClientSession")
@patch("onyx_client.OnyxClient.authorize")
@patch("onyx_client.OnyxClient.verify")
@pytest.mark.asyncio
async def test_exchange_code(mock_verify, mock_authorize, mock_session):
    config = await exchange_code("code", mock_session)
    assert config is not None
    assert mock_authorize.called
    assert mock_verify.called


@patch("aiohttp.ClientSession")
@patch("onyx_client.OnyxClient.authorize")
@patch("onyx_client.OnyxClient.verify")
@pytest.mark.asyncio
async def test_exchange_code_failed(mock_verify, mock_authorize, mock_session):
    mock_verify.return_value = False
    config = await exchange_code("code", mock_session)
    assert config is None
    assert mock_authorize.called
    assert mock_verify.called
