"""Tests that the access token never reaches the log or an exception."""

import asyncio
import gc
import logging
import traceback
from unittest.mock import AsyncMock, patch

import aiohttp
import pytest
import pytest_asyncio
from aioresponses import aioresponses

from onyx_client.client import OnyxClient
from onyx_client.configuration.configuration import Configuration
from onyx_client.stream.events import Resynced, Snapshot
from onyx_client.utils.const import API_URL, API_VERSION

TOKEN = "s3cr3t-t0k3n-value"
URL = f"{API_URL}/box/finger/api/{API_VERSION}"


@pytest_asyncio.fixture
async def client():
    async with aiohttp.ClientSession() as session:
        yield OnyxClient(Configuration("finger", TOKEN), session)


@pytest.fixture
def mocked():
    with aioresponses() as m:
        yield m


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [404, 500, 502])
async def test_stream_reconnect_log_has_no_token(mocked, client, caplog, status):
    mocked.get(f"{URL}/clock", status=401, repeat=True)
    mocked.get(f"{URL}/events", status=status)
    mocked.get(f"{URL}/events", status=200, body="event: snapshot\ndata: {}\n\n")
    mocked.get(f"{URL}/events", status=200, body="event: snapshot\ndata: {}\n\n")
    with (
        caplog.at_level(logging.DEBUG),
        patch("onyx_client.client.asyncio.sleep", new_callable=AsyncMock),
    ):
        stream = client.stream()
        events = [await anext(stream) for _ in range(2)]
        await stream.aclose()
    assert isinstance(events[0], Snapshot)
    assert isinstance(events[1], Resynced)
    assert f"status={status}" in caplog.text
    assert "ClientResponseError" in caplog.text
    assert TOKEN not in caplog.text
    assert "Authorization" not in caplog.text
    assert TOKEN not in events[1].reason


def assert_no_token(exc: BaseException):
    assert TOKEN not in repr(exc)
    assert TOKEN not in repr(exc.args)
    assert TOKEN not in str(exc)
    assert TOKEN not in "".join(traceback.format_exception(exc))


@pytest.mark.asyncio
async def test_stream_rejected_credentials_carry_no_token(mocked, client):
    mocked.get(f"{URL}/clock", status=401)
    mocked.get(f"{URL}/events", status=401)
    with pytest.raises(aiohttp.ClientResponseError) as info:
        await anext(client.stream())
    assert info.value.status == 401
    assert_no_token(info.value)


@pytest.mark.asyncio
async def test_non_json_response_carries_no_token(mocked, client):
    mocked.get(f"{URL}/devices", status=200, body="<html>", content_type="text/html")
    with pytest.raises(aiohttp.ContentTypeError) as info:
        await client.devices()
    assert_no_token(info.value)


@pytest.mark.asyncio
async def test_unretrieved_task_exception_has_no_token(mocked, client, caplog):
    mocked.get(f"{URL}/clock", status=401)
    mocked.get(f"{URL}/events", status=401)
    task = asyncio.create_task(anext(client.stream()))
    await asyncio.wait([task])
    with caplog.at_level(logging.ERROR, logger="asyncio"):
        del task
        gc.collect()
    assert "never retrieved" in caplog.text
    assert TOKEN not in caplog.text


def test_client_logger_masks_leaked_header(caplog):
    logger = logging.getLogger("onyx_client.client")
    with caplog.at_level(logging.DEBUG):
        logger.error("oops %s", {"Authorization": f"Bearer {TOKEN}"})
    assert TOKEN not in caplog.text
