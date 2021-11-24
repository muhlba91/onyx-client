"""Tests for response utils."""
from unittest.mock import patch

from onyx_client.utils.response import check


@patch("aiohttp.ClientResponse")
def test_check(mock_response):
    mock_response.status = 200
    assert check(mock_response)


@patch("aiohttp.ClientResponse")
def test_check_error(mock_response):
    mock_response.status = 401
    assert not check(mock_response)
