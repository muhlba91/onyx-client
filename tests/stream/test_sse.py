"""Tests for the Server-Sent Events parser."""

import pytest

from onyx_client.stream.sse import parse


async def lines(*values: str):
    for value in values:
        yield value


async def events(*values: str) -> list:
    return [event async for event in parse(lines(*values))]


@pytest.mark.asyncio
async def test_parse():
    assert await events(
        "event: pulse", "data: 1", "", "event: patch", "data: {}", ""
    ) == [
        ("pulse", "1"),
        ("patch", "{}"),
    ]


@pytest.mark.asyncio
async def test_parse_multi_line_data():
    assert await events("event: snapshot", "data: {", "data:}", "") == [
        ("snapshot", "{\n}")
    ]


@pytest.mark.asyncio
async def test_parse_default_event():
    assert await events("data: 1", "") == [("message", "1")]


@pytest.mark.asyncio
async def test_parse_ignores_comments_and_unknown_fields():
    assert await events(": comment", "id: 1", "retry: 10", "data: 1", "") == [
        ("message", "1")
    ]


@pytest.mark.asyncio
async def test_parse_ignores_events_without_data():
    assert await events("event: patch", "", "data: 1", "") == [("message", "1")]


@pytest.mark.asyncio
async def test_parse_ignores_incomplete_event():
    assert await events("event: patch", "data: 1") == []


@pytest.mark.asyncio
async def test_parse_keeps_further_spaces():
    assert await events("data:  1", "") == [("message", " 1")]


@pytest.mark.asyncio
async def test_parse_empty_event_name():
    assert await events("event:", "data: 1", "") == [("message", "1")]
