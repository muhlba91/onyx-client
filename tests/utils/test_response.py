"""Tests for response utils."""

from unittest.mock import MagicMock

from aiohttp import ClientResponse

from onyx_client.utils.response import check


def test_check():
    mock_response = MagicMock(spec=ClientResponse)
    mock_response.status = 200
    assert check(mock_response)


def test_check_error():
    mock_response = MagicMock(spec=ClientResponse)
    mock_response.status = 401
    assert not check(mock_response)

    mock_response.status = 201
    assert not check(mock_response)

    mock_response.status = 199
    assert not check(mock_response)

    mock_response.status = 500
    assert not check(mock_response)
