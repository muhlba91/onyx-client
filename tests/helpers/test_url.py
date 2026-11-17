"""Tests for the Onyx Client URL helper."""

from unittest.mock import patch

import aiohttp
import pytest
import pytest_asyncio
from aiohttp import web
from aiohttp.test_utils import TestServer
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

    @pytest_asyncio.fixture
    def helper_local(self, session) -> UrlHelper:
        yield UrlHelper(
            Configuration("finger", "token", local_address="localhost"), session
        )

    def test_headers(self, helper):
        headers = helper._headers
        for header in API_HEADERS:
            assert header in headers
        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer token"

    def test_base_url(self, helper):
        assert helper._base_url() == f"{API_URL}/box/finger/api/{API_VERSION}"

    def test_base_url_local(self, helper_local):
        assert helper_local._base_url() == f"https://localhost/api/{API_VERSION}"

    def test_base_url_without_version(self, helper):
        assert helper._base_url(with_api=False) == f"{API_URL}/box/finger/api"

    def test_url(self, helper):
        assert helper._url("/path") == f"{API_URL}/box/finger/api/{API_VERSION}/path"

    def test_url_local(self, helper_local):
        assert helper_local._url("/path") == f"https://localhost/api/{API_VERSION}/path"

    def test_url_without_version(self, helper):
        assert helper._url("/path", with_api=False) == f"{API_URL}/box/finger/api/path"

    def test_url_default_params(self, helper):
        assert helper._url() == f"{API_URL}/box/finger/api/{API_VERSION}"
        assert helper._url(with_api=False) == f"{API_URL}/box/finger/api"

    @pytest.mark.asyncio
    async def test_perform_get_request(self, mock_response, helper):
        with patch.object(
            helper.client_session, "get", wraps=helper.client_session.get
        ) as mock_get:
            mock_response.get(
                f"{API_URL}/box/finger/api/{API_VERSION}/path", status=200, payload={}
            )
            response = await helper.perform_get_request("/path")
            assert response is not None
            mock_get.assert_called_once_with(
                f"{API_URL}/box/finger/api/{API_VERSION}/path",
                headers=helper._headers,
                ssl=True,
            )

    @pytest.mark.asyncio
    async def test_perform_get_request_with_local_address(
        self, mock_response, helper_local
    ):
        with patch.object(
            helper_local.client_session, "get", wraps=helper_local.client_session.get
        ) as mock_get:
            mock_response.get(
                f"https://localhost/api/{API_VERSION}/path", status=200, payload={}
            )
            response = await helper_local.perform_get_request("/path")
            assert response is not None
            mock_get.assert_called_once_with(
                f"https://localhost/api/{API_VERSION}/path",
                headers=helper_local._headers,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_perform_get_request_error(self, mock_response, helper):
        mock_response.get(f"{API_URL}/box/finger/api/{API_VERSION}/path", status=401)
        response = await helper.perform_get_request("/path")
        assert response is None

    @pytest.mark.asyncio
    async def test_perform_delete_request(self, mock_response, helper):
        with patch.object(
            helper.client_session, "delete", wraps=helper.client_session.delete
        ) as mock_delete:
            mock_response.delete(
                f"{API_URL}/box/finger/api/{API_VERSION}/path", status=200, payload={}
            )
            response = await helper.perform_delete_request("/path")
            assert response is not None
            mock_delete.assert_called_once_with(
                f"{API_URL}/box/finger/api/{API_VERSION}/path",
                headers=helper._headers,
                ssl=True,
            )

    @pytest.mark.asyncio
    async def test_perform_delete_request_with_local_address(
        self, mock_response, helper_local
    ):
        with patch.object(
            helper_local.client_session,
            "delete",
            wraps=helper_local.client_session.delete,
        ) as mock_delete:
            mock_response.delete(
                f"https://localhost/api/{API_VERSION}/path", status=200, payload={}
            )
            response = await helper_local.perform_delete_request("/path")
            assert response is not None
            mock_delete.assert_called_once_with(
                f"https://localhost/api/{API_VERSION}/path",
                headers=helper_local._headers,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_perform_delete_request_error(self, mock_response, helper):
        mock_response.delete(f"{API_URL}/box/finger/api/{API_VERSION}/path", status=401)
        response = await helper.perform_delete_request("/path")
        assert response is None

    @pytest.mark.asyncio
    async def test_perform_post_request(self, mock_response, helper):
        with patch.object(
            helper.client_session, "post", wraps=helper.client_session.post
        ) as mock_post:
            mock_response.post(
                f"{API_URL}/box/finger/api/{API_VERSION}/path", status=200, payload={}
            )
            payload = {"test": 1}
            response = await helper.perform_post_request("/path", payload)
            assert response is not None
            mock_post.assert_called_once_with(
                f"{API_URL}/box/finger/api/{API_VERSION}/path",
                json=payload,
                headers=helper._headers,
                ssl=True,
            )

    @pytest.mark.asyncio
    async def test_perform_post_request_with_local_address(
        self, mock_response, helper_local
    ):
        with patch.object(
            helper_local.client_session, "post", wraps=helper_local.client_session.post
        ) as mock_post:
            mock_response.post(
                f"https://localhost/api/{API_VERSION}/path", status=200, payload={}
            )
            payload = {"test": 1}
            response = await helper_local.perform_post_request("/path", payload)
            assert response is not None
            mock_post.assert_called_once_with(
                f"https://localhost/api/{API_VERSION}/path",
                json=payload,
                headers=helper_local._headers,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_perform_post_request_error(self, mock_response, helper):
        mock_response.post(f"{API_URL}/box/finger/api/{API_VERSION}/path", status=401)
        response = await helper.perform_post_request("/path", {})
        assert response is None

    @pytest.mark.asyncio
    async def test_perform_post_request_without_data(self, mock_response, helper):
        mock_response.post(
            f"{API_URL}/box/finger/api/{API_VERSION}/path", status=200, payload={}
        )
        assert await helper.perform_post_request("/path") == {}

    @pytest.mark.asyncio
    async def test_perform_status_request(self, mock_response, helper):
        mock_response.post(f"{API_URL}/box/finger/api/{API_VERSION}/logout", status=204)
        assert await helper.perform_status_request("POST", "/logout") == 204

    @pytest.mark.asyncio
    async def test_perform_status_request_with_local_address(
        self, mock_response, helper_local
    ):
        with patch.object(
            helper_local.client_session,
            "request",
            wraps=helper_local.client_session.request,
        ) as mock_request:
            mock_response.get(f"https://localhost/api/{API_VERSION}/clock", status=401)
            assert await helper_local.perform_status_request("GET", "/clock") == 401
            mock_request.assert_called_once_with(
                "GET",
                f"https://localhost/api/{API_VERSION}/clock",
                headers=helper_local._headers,
                ssl=False,
            )

    def test_url_deprecated_api_version(self, session):
        helper = UrlHelper(Configuration("finger", "token", api_version="v3"), session)
        assert helper._url("/path") == f"{API_URL}/box/finger/api/v3/path"

    @pytest.mark.asyncio
    async def test_start_stream(self, mock_response, helper):
        with patch.object(
            helper.client_session, "get", wraps=helper.client_session.get
        ) as mock_get:
            mock_response.get(
                f"{API_URL}/box/finger/api/{API_VERSION}/events",
                status=200,
                body="event: pulse\r\ndata: 1 \n\n",
            )
            lines = [line async for line in helper.start_stream("/events")]
            assert lines == ["event: pulse", "data: 1 ", ""]
            assert helper._stream_response is None
            mock_get.assert_called_once_with(
                f"{API_URL}/box/finger/api/{API_VERSION}/events",
                headers=helper._headers,
                timeout=aiohttp.ClientTimeout(
                    total=None, sock_connect=10, sock_read=90
                ),
                ssl=True,
            )

    @pytest.mark.asyncio
    async def test_start_stream_with_local_address(self, mock_response, helper_local):
        with patch.object(
            helper_local.client_session, "get", wraps=helper_local.client_session.get
        ) as mock_get:
            mock_response.get(
                f"https://localhost/api/{API_VERSION}/events",
                status=200,
                body="data: {}",
            )
            lines = [line async for line in helper_local.start_stream("/events")]
            assert lines == ["data: {}"]
            mock_get.assert_called_once_with(
                f"https://localhost/api/{API_VERSION}/events",
                headers=helper_local._headers,
                timeout=aiohttp.ClientTimeout(
                    total=None, sock_connect=10, sock_read=90
                ),
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_start_stream_empty(self, mock_response, helper):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events", status=200, body=""
        )
        assert [line async for line in helper.start_stream("/events")] == []

    @pytest.mark.asyncio
    async def test_start_stream_error(self, mock_response, helper):
        mock_response.get(f"{API_URL}/box/finger/api/{API_VERSION}/events", status=401)
        with pytest.raises(aiohttp.ClientResponseError):
            async for _ in helper.start_stream("/events"):
                pass

    @pytest.mark.asyncio
    async def test_start_stream_fallback_decoding(self, mock_response, helper):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=200,
            body=b"\xff\n",
        )
        assert [line async for line in helper.start_stream("/events")] == ["\ufffd"]

    @pytest.mark.asyncio
    async def test_close_stream(self, mock_response, helper):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=200,
            body="data: 1\n\ndata: 2\n\n",
        )
        async for _ in helper.start_stream("/events"):
            response = helper._stream_response
            helper.close_stream()
            assert response.closed
            break

    def test_close_stream_without_stream(self, helper):
        helper.close_stream()
        assert helper._stream_response is None

    @pytest.mark.asyncio
    async def test_start_stream_long_lines(self, session):
        snapshot = "data: " + "x" * 300_000

        async def handler(request):
            response = web.StreamResponse()
            await response.prepare(request)
            await response.write(snapshot[:1000].encode())
            await response.write(f"{snapshot[1000:]}\r\n\nevent: pulse".encode())
            return response

        app = web.Application()
        app.router.add_get("/events", handler)
        async with TestServer(app) as server:
            helper = UrlHelper(Configuration("finger", "token"), session)
            with patch.object(
                helper, "_url", return_value=str(server.make_url("/events"))
            ):
                lines = [line async for line in helper.start_stream("/events")]
        assert lines == [snapshot, "", "event: pulse"]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("method", ["get", "delete", "post"])
    async def test_non_json_response_carries_no_token(
        self, mock_response, session, method
    ):
        helper = UrlHelper(Configuration("finger", "t0k3n-dummy"), session)
        getattr(mock_response, method)(
            f"{API_URL}/box/finger/api/{API_VERSION}/path",
            status=200,
            body="<html>",
            content_type="text/html",
        )
        with pytest.raises(aiohttp.ContentTypeError) as info:
            await getattr(helper, f"perform_{method}_request")("/path")
        assert "t0k3n-dummy" not in repr(info.value)
        assert "t0k3n-dummy" not in repr(info.value.args)
        assert "t0k3n-dummy" not in str(info.value)

    @pytest.mark.asyncio
    async def test_start_stream_error_carries_no_token(self, mock_response, session):
        helper = UrlHelper(Configuration("finger", "t0k3n-dummy"), session)
        mock_response.get(f"{API_URL}/box/finger/api/{API_VERSION}/events", status=401)
        with pytest.raises(aiohttp.ClientResponseError) as info:
            async for _ in helper.start_stream("/events"):
                pass
        assert "t0k3n-dummy" not in repr(info.value)
        assert "t0k3n-dummy" not in repr(info.value.args)
