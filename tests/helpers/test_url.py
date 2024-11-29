"""Tests for the Onyx Client URL helper."""

import aiohttp
import pytest
import pytest_asyncio

from aioresponses import aioresponses

from onyx_client.configuration.configuration import Configuration
from onyx_client.helpers.url import UrlHelper
from onyx_client.utils.const import API_HEADERS, API_URL, API_VERSION


class TestUrlHelper:
    @pytest_asyncio.fixture
    async def session(self) -> aiohttp.ClientSession:
        sess = aiohttp.ClientSession()
        yield sess
        await sess.close()

    @pytest_asyncio.fixture
    def mock_response(self):
        with aioresponses() as mocked:
            yield mocked

    @pytest_asyncio.fixture
    def helper(self, session) -> UrlHelper:
        yield UrlHelper(Configuration("finger", "token"), session)

    def test_headers(self, helper):
        headers = helper._headers
        for header in API_HEADERS:
            assert header in headers
        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer token"

    def test_base_url(self, helper):
        assert helper._base_url() == f"{API_URL}/box/finger/api/{API_VERSION}"

    def test_base_url_without_version(self, helper):
        assert helper._base_url(with_api=False) == f"{API_URL}/box/finger/api"

    def test_url(self, helper):
        assert helper._url("/path") == f"{API_URL}/box/finger/api/{API_VERSION}/path"

    def test_url_without_version(self, helper):
        assert helper._url("/path", with_api=False) == f"{API_URL}/box/finger/api/path"

    @pytest.mark.asyncio
    async def test_perform_get_request(self, mock_response, helper):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/path", status=200, payload={}
        )
        response = await helper.perform_get_request("/path")
        assert response is not None

    @pytest.mark.asyncio
    async def test_perform_get_request_error(self, mock_response, helper):
        mock_response.get(f"{API_URL}/box/finger/api/{API_VERSION}/path", status=401)
        response = await helper.perform_get_request("/path")
        assert response is None

    @pytest.mark.asyncio
    async def test_perform_delete_request(self, mock_response, helper):
        mock_response.delete(
            f"{API_URL}/box/finger/api/{API_VERSION}/path", status=200, payload={}
        )
        response = await helper.perform_delete_request("/path")
        assert response is not None

    @pytest.mark.asyncio
    async def test_perform_delete_request_error(self, mock_response, helper):
        mock_response.delete(f"{API_URL}/box/finger/api/{API_VERSION}/path", status=401)
        response = await helper.perform_delete_request("/path")
        assert response is None

    @pytest.mark.asyncio
    async def test_perform_post_request(self, mock_response, helper):
        mock_response.post(
            f"{API_URL}/box/finger/api/{API_VERSION}/path", status=200, payload={}
        )
        response = await helper.perform_post_request("/path", {})
        assert response is not None

    @pytest.mark.asyncio
    async def test_perform_post_request_error(self, mock_response, helper):
        mock_response.post(f"{API_URL}/box/finger/api/{API_VERSION}/path", status=401)
        response = await helper.perform_post_request("/path", {})
        assert response is None

    @pytest.mark.asyncio
    async def test_start_stream(self, mock_response, helper):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=200,
            body="data: {  }",
        )
        index = 1
        async for data in helper.start_stream("/events"):
            assert len(data) > 0
            index += 1
        assert index == 2

    @pytest.mark.asyncio
    async def test_start_stream_none(self, mock_response, helper):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=200,
            body="",
        )
        index = 1
        async for data in helper.start_stream("/events"):
            index += 1
        assert index == 1

    @pytest.mark.asyncio
    async def test_start_stream_error(self, mock_response, helper):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=500,
            body="",
        )
        index = 1
        async for data in helper.start_stream("/events"):
            assert data is None
            index += 1
        assert index == 2
