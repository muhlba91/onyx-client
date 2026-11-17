"""Tests for the Onyx Client."""

import asyncio
import json
import logging
from unittest.mock import AsyncMock, patch

import aiohttp
import pytest
import pytest_asyncio
from aioresponses import aioresponses
from yarl import URL as YarlURL

from onyx_client.client import OnyxClient, create
from onyx_client.configuration.configuration import Configuration
from onyx_client.data.device_command import DeviceCommand
from onyx_client.device.shutter import Shutter
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType
from onyx_client.enum.verify_result import VerifyResult
from onyx_client.stream.events import (
    DeviceChanged,
    DeviceRemoved,
    Pulse,
    Resynced,
    Snapshot,
)
from onyx_client.utils.const import API_URL, API_VERSION

URL = f"{API_URL}/box/finger/api/{API_VERSION}"
URL_EVENTS = YarlURL(f"{URL}/events")
DEVICE = {"name": "Shutter", "type": "rollershutter"}


def sse(event: str, data) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


class StopStream(Exception):
    """Raised by the mocked backoff to end an endless stream."""


@patch("aiohttp.ClientSession")
def test_create_client(mock_session):
    client = create(
        fingerprint="finger", access_token="token", client_session=mock_session
    )
    assert client.url_helper.client_session == mock_session
    assert client.config.fingerprint == "finger"
    assert client.config.access_token == "token"
    assert client.config.api_version == API_VERSION
    assert client.clock_offset == 0
    assert not client._close_session


@patch("aiohttp.ClientSession")
def test_create_client_with_local_address(mock_session):
    client = create(
        fingerprint="finger",
        access_token="token",
        client_session=mock_session,
        local_address="192.168.1.1",
    )
    assert client.config.local_address == "192.168.1.1"


@patch("aiohttp.ClientSession")
def test_create_client_with_api_version(mock_session):
    client = create(
        fingerprint="finger",
        access_token="token",
        client_session=mock_session,
        api_version="v3",
    )
    assert client.config.api_version == "v3"


@patch("aiohttp.ClientSession")
def test_create_client_with_config(mock_session):
    config = Configuration("finger", "token")
    client = create(config=config, client_session=mock_session)
    assert client.config is config
    assert client.url_helper.config is config


@patch("aiohttp.ClientSession")
def test_create_client_without_session(mock_session):
    client = create(fingerprint="finger", access_token="token")
    assert client.client_session is not None
    assert client._close_session


class TestOnyxClient:
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
    def client(self, session) -> OnyxClient:
        yield OnyxClient(Configuration("finger", "token"), session)

    @pytest_asyncio.fixture
    def mock_sleep(self):
        with patch("onyx_client.client.asyncio.sleep", new_callable=AsyncMock) as sleep:
            yield sleep

    def test_init(self, session, caplog):
        client = OnyxClient(Configuration("finger", "token"), session)
        assert client.clock_offset == 0
        assert not client._close_session
        assert not client._resync_requested
        assert "deprecated" not in caplog.text

    def test_init_deprecated_api_version(self, session, caplog):
        OnyxClient(Configuration("finger", "token", api_version="v3"), session)
        assert "ONYX API v3 is deprecated" in caplog.text

    @pytest.mark.asyncio
    async def test_verify(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/versions",
            status=200,
            payload={"versions": ["v3", API_VERSION]},
        )
        mock_response.get(f"{URL}/clock", status=200, payload={})
        assert await client.verify() == VerifyResult.OK

    @pytest.mark.asyncio
    async def test_verify_unsupported_api_version(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/versions",
            status=200,
            payload={"versions": ["v1", "v3"]},
        )
        assert await client.verify() == VerifyResult.VERSION_UNSUPPORTED

    @pytest.mark.asyncio
    async def test_verify_deprecated_api_version(self, mock_response, session):
        client = OnyxClient(Configuration("finger", "token", api_version="v3"), session)
        mock_response.get(
            f"{API_URL}/box/finger/api/versions",
            status=200,
            payload={"versions": ["v1", "v3"]},
        )
        mock_response.get(f"{API_URL}/box/finger/api/v3/clock", status=200)
        assert await client.verify() == VerifyResult.OK

    @pytest.mark.asyncio
    async def test_verify_versions_error(self, mock_response, client):
        mock_response.get(f"{API_URL}/box/finger/api/versions", status=500)
        assert await client.verify() == VerifyResult.UNREACHABLE

    @pytest.mark.asyncio
    async def test_verify_connection_error(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/versions",
            exception=aiohttp.ClientConnectionError(),
        )
        assert await client.verify() == VerifyResult.UNREACHABLE

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("status", "expected"),
        [
            (401, VerifyResult.UNAUTHORIZED),
            (403, VerifyResult.UNAUTHORIZED),
            (500, VerifyResult.UNREACHABLE),
        ],
    )
    async def test_verify_clock_status(self, mock_response, client, status, expected):
        mock_response.get(
            f"{API_URL}/box/finger/api/versions",
            status=200,
            payload={"versions": [API_VERSION]},
        )
        mock_response.get(f"{URL}/clock", status=status)
        assert await client.verify() == expected

    @pytest.mark.asyncio
    async def test_devices(self, mock_response, client, captured):
        mock_response.get(
            f"{URL}/devices",
            status=200,
            payload=json.loads(captured("devices-v6.json")),
        )
        devices = await client.devices()
        assert len(devices) == 8
        assert all(isinstance(device, Shutter) for device in devices)
        assert devices[0].identifier == "00000000-0000-4000-8000-000000000001"
        assert devices[0].tint == "#F3835D"

    @pytest.mark.asyncio
    async def test_devices_error(self, mock_response, client):
        mock_response.get(f"{URL}/devices", status=401)
        assert await client.devices() is None

    @pytest.mark.asyncio
    async def test_device(self, mock_response, client, captured):
        identifier = "00000000-0000-4000-8000-000000000001"
        mock_response.get(
            f"{URL}/devices/{identifier}",
            status=200,
            payload=json.loads(captured(f"details/{identifier}.json")),
        )
        device = await client.device(identifier)
        assert isinstance(device, Shutter)
        assert device.identifier == identifier
        assert device.device_type == DeviceType.RAFFSTORE_90
        assert device.actions == [Action.CLOSE, Action.OPEN, Action.STOP, Action.WINK]
        assert device.system_state.value == "ok"

    @pytest.mark.asyncio
    async def test_device_error(self, mock_response, client):
        mock_response.get(f"{URL}/devices/device", status=401)
        assert await client.device("device") is None

    @pytest.mark.asyncio
    async def test_supported_versions(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/versions",
            status=200,
            payload={"versions": [API_VERSION, "v2"]},
        )
        versions = await client.supported_versions()
        assert versions is not None
        assert versions.supports(API_VERSION)
        assert versions.supports("v2")

    @pytest.mark.asyncio
    async def test_supported_versions_none(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/versions",
            status=200,
            payload={},
        )
        versions = await client.supported_versions()
        assert versions is not None
        assert len(versions.versions) == 0

    @pytest.mark.asyncio
    async def test_supported_versions_error(self, mock_response, client):
        mock_response.get(f"{API_URL}/box/finger/api/versions", status=401)
        versions = await client.supported_versions()
        assert versions is None

    @pytest.mark.asyncio
    async def test_date_information(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/clock",
            status=200,
            payload={"time": 100.5, "zone": "Europe", "zone_offset": 100},
        )
        date = await client.date_information()
        assert date is not None
        assert date.time == 100.5
        assert date.timezone == "Europe"
        assert date.timezone_offset == 100

    @pytest.mark.asyncio
    async def test_date_information_none(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/clock",
            status=200,
            payload={},
        )
        date = await client.date_information()
        assert date is not None
        assert date.time == 0
        assert date.timezone is None
        assert date.timezone_offset == 0

    @pytest.mark.asyncio
    async def test_date_information_error(self, mock_response, client):
        mock_response.get(f"{API_URL}/box/finger/api/{API_VERSION}/clock", status=401)
        date = await client.date_information()
        assert date is None

    @pytest.mark.asyncio
    async def test_send_command(self, mock_response, client):
        with patch.object(
            client.url_helper,
            "perform_post_request",
            wraps=client.url_helper.perform_post_request,
        ) as mock_post:
            mock_response.post(
                f"{API_URL}/box/finger/api/{API_VERSION}/devices/device/command",
                status=200,
                payload={},
            )
            cmd = DeviceCommand(action=Action.STOP)
            assert await client.send_command("device", cmd)
            mock_post.assert_called_once_with(
                "/devices/device/command", {"action": "stop"}
            )

    @pytest.mark.asyncio
    async def test_send_command_error(self, mock_response, client):
        with patch.object(
            client.url_helper,
            "perform_post_request",
            wraps=client.url_helper.perform_post_request,
        ) as mock_post:
            mock_response.post(
                f"{API_URL}/box/finger/api/{API_VERSION}/devices/device/command",
                status=401,
            )
            cmd = DeviceCommand(action=Action.STOP)
            assert not await client.send_command("device", cmd)
            mock_post.assert_called_once_with(
                "/devices/device/command", {"action": "stop"}
            )

    @pytest.mark.asyncio
    async def test_cancel_command(self, mock_response, client):
        with patch.object(
            client.url_helper,
            "perform_delete_request",
            wraps=client.url_helper.perform_delete_request,
        ) as mock_delete:
            mock_response.delete(
                f"{API_URL}/box/finger/api/{API_VERSION}/devices/device/command",
                status=200,
                payload={},
            )
            assert await client.cancel_command("device")
            mock_delete.assert_called_once_with("/devices/device/command")

    @pytest.mark.asyncio
    async def test_cancel_command_error(self, mock_response, client):
        mock_response.delete(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device/command", status=401
        )
        assert not await client.cancel_command("device")

    @pytest.mark.asyncio
    async def test_groups(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups",
            status=200,
            payload={
                "group1": {"name": "group1", "devices": ["device1"]},
                "group2": {"name": "group2", "devices": ["device1", "device2"]},
            },
        )
        groups = await client.groups()
        assert groups is not None
        assert len(groups) == 2
        groups1 = list(filter(lambda dev: dev.identifier == "group1", groups))
        assert len(groups1) == 1
        group1 = groups1[0]
        assert group1 is not None
        assert group1.identifier == "group1"
        assert group1.name == "group1"
        assert group1.devices == ["device1"]
        groups2 = list(filter(lambda dev: dev.identifier == "group2", groups))
        assert len(groups2) == 1
        group2 = groups2[0]
        assert group2 is not None
        assert group2.identifier == "group2"
        assert group2.name == "group2"
        assert group2.devices == ["device1", "device2"]

    @pytest.mark.asyncio
    async def test_groups_none(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups",
            status=200,
            payload={
                "group1": {},
            },
        )
        groups = await client.groups()
        assert groups is not None
        assert len(groups) == 1
        group1 = groups[0]
        assert group1 is not None
        assert group1.identifier == "group1"
        assert group1.name is None
        assert len(group1.devices) == 0

    @pytest.mark.asyncio
    async def test_groups_error(self, mock_response, client):
        mock_response.get(f"{API_URL}/box/finger/api/{API_VERSION}/groups", status=401)
        groups = await client.groups()
        assert groups is None

    @pytest.mark.asyncio
    async def test_group(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups/group",
            status=200,
            payload={"name": "group", "devices": ["device"]},
        )
        group = await client.group("group")
        assert group is not None
        assert group.identifier == "group"
        assert group.name == "group"
        assert group.devices == ["device"]

    @pytest.mark.asyncio
    async def test_group_none(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups/group",
            status=200,
            payload={},
        )
        group = await client.group("group")
        assert group is not None
        assert group.name is None
        assert len(group.devices) == 0

    @pytest.mark.asyncio
    async def test_group_error(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups/group", status=401
        )
        group = await client.group("group")
        assert group is None

    @pytest.mark.asyncio
    async def test_send_group_command(self, mock_response, client):
        with patch.object(
            client.url_helper,
            "perform_post_request",
            wraps=client.url_helper.perform_post_request,
        ) as mock_post:
            mock_response.post(
                f"{API_URL}/box/finger/api/{API_VERSION}/groups/group/command",
                status=200,
                payload={"results": {"device": {"status_code": 200}}},
            )
            cmd = DeviceCommand(action=Action.STOP)
            assert await client.send_group_command("group", cmd)
            mock_post.assert_called_once_with(
                "/groups/group/command", {"action": "stop"}
            )

    @pytest.mark.asyncio
    async def test_send_group_command_no_results(self, mock_response, client):
        mock_response.post(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups/group/command",
            status=200,
            payload={"results": {}},
        )
        assert await client.send_group_command(
            "group", DeviceCommand(action=Action.STOP)
        )

    @pytest.mark.asyncio
    async def test_send_group_command_none(self, mock_response, client):
        mock_response.post(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups/group/command",
            status=200,
            payload={},
        )
        assert await client.send_group_command(
            "group", DeviceCommand(action=Action.STOP)
        )

    @pytest.mark.asyncio
    async def test_send_group_command_no_status_code(self, mock_response, client):
        mock_response.post(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups/group/command",
            status=200,
            payload={"results": {"device": {}}},
        )
        assert not await client.send_group_command(
            "group", DeviceCommand(action=Action.STOP)
        )

    @pytest.mark.asyncio
    async def test_send_group_command_device_error(self, mock_response, client):
        mock_response.post(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups/group/command",
            status=200,
            payload={
                "results": {
                    "device": {"status_code": 401},
                    "other": {"status_code": 200},
                }
            },
        )
        assert not await client.send_group_command(
            "group", DeviceCommand(action=Action.STOP)
        )

    @pytest.mark.asyncio
    async def test_send_group_command_single_device_error(self, mock_response, client):
        mock_response.post(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups/group/command",
            status=200,
            payload={
                "results": {
                    "device": {"status_code": 401},
                }
            },
        )
        assert not await client.send_group_command(
            "group", DeviceCommand(action=Action.STOP)
        )

    @pytest.mark.asyncio
    async def test_send_group_command_all_devices_success(self, mock_response, client):
        mock_response.post(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups/group/command",
            status=200,
            payload={
                "results": {
                    "device": {"status_code": 200},
                    "other": {"status_code": 200},
                }
            },
        )
        assert await client.send_group_command(
            "group", DeviceCommand(action=Action.STOP)
        )

    @pytest.mark.asyncio
    async def test_send_group_command_error(self, mock_response, client):
        mock_response.post(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups/group/command", status=401
        )
        assert not await client.send_group_command(
            "group", DeviceCommand(action=Action.STOP)
        )

    @pytest.mark.asyncio
    async def test_cancel_group_command(self, mock_response, client):
        with patch.object(
            client.url_helper,
            "perform_delete_request",
            wraps=client.url_helper.perform_delete_request,
        ) as mock_delete:
            mock_response.delete(
                f"{API_URL}/box/finger/api/{API_VERSION}/groups/group/command",
                status=200,
                payload={},
            )
            assert await client.cancel_group_command("group")
            mock_delete.assert_called_once_with("/groups/group/command")

    @pytest.mark.asyncio
    async def test_cancel_group_command_error(self, mock_response, client):
        mock_response.delete(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups/group/command", status=401
        )
        assert not await client.cancel_group_command("group")

    @pytest.mark.asyncio
    async def test_automations(self, mock_response, client):
        mock_response.get(
            f"{URL}/automations",
            status=200,
            payload=[
                {"id": "a1", "name": "Wind", "type": "wind", "enabled": True},
                {"id": "a2", "enabled": False},
            ],
        )
        automations = await client.automations()
        assert [automation.identifier for automation in automations] == ["a1", "a2"]
        assert automations[0].enabled
        assert not automations[1].enabled

    @pytest.mark.asyncio
    async def test_automations_error(self, mock_response, client):
        mock_response.get(f"{URL}/automations", status=404)
        assert await client.automations() is None

    @pytest.mark.asyncio
    async def test_enable_automation(self, mock_response, client):
        mock_response.post(
            f"{URL}/automations/a1/enable",
            status=200,
            payload={"id": "a1", "enabled": True},
        )
        automation = await client.enable_automation("a1")
        assert automation.identifier == "a1"
        assert automation.enabled

    @pytest.mark.asyncio
    async def test_disable_automation_encodes_identifier(self, mock_response, client):
        identifier = "http://o.hella.info/d/1ff1014/scenarios?type=info.hella.onyx.wind"
        mock_response.post(
            f"{URL}/automations/http%3A%2F%2Fo.hella.info%2Fd%2F1ff1014%2Fscenarios%3Ftype%3Dinfo.hella.onyx.wind/disable",
            status=200,
            payload={"id": identifier, "enabled": False},
        )
        automation = await client.disable_automation(identifier)
        assert automation.identifier == identifier
        assert not automation.enabled

    @pytest.mark.asyncio
    async def test_enable_automation_error(self, mock_response, client):
        mock_response.post(f"{URL}/automations/a1/enable", status=404)
        assert await client.enable_automation("a1") is None

    @pytest.mark.asyncio
    async def test_update_status(self, mock_response, client, captured):
        mock_response.get(
            f"{URL}/update", status=200, payload=json.loads(captured("update.json"))
        )
        status = await client.update_status()
        assert status.current == "2.13.4-0-geb8e366"
        assert status.available_version is None

    @pytest.mark.asyncio
    async def test_update_status_error(self, mock_response, client):
        mock_response.get(f"{URL}/update", status=404)
        assert await client.update_status() is None

    @pytest.mark.asyncio
    async def test_check_for_update(self, mock_response, client):
        mock_response.post(
            f"{URL}/update/check",
            status=200,
            payload={"current": "2.13.0", "available": {"version": "2.14.0"}},
        )
        status = await client.check_for_update()
        assert status.available_version == "2.14.0"

    @pytest.mark.asyncio
    async def test_check_for_update_error(self, mock_response, client):
        mock_response.post(f"{URL}/update/check", status=500)
        assert await client.check_for_update() is None

    @pytest.mark.asyncio
    async def test_install_update(self, mock_response, client):
        mock_response.post(
            f"{URL}/update/install",
            status=200,
            payload={"current": "2.13.0", "available": {"version": "2.14.0"}},
        )
        status = await client.install_update()
        assert status.current == "2.13.0"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("status", "expected"), [(204, True), (401, True), (503, False)]
    )
    async def test_logout(self, mock_response, client, status, expected):
        mock_response.post(f"{URL}/logout", status=status)
        assert await client.logout() == expected

    def test_now(self, client):
        client.clock_offset = 0.25
        with patch("onyx_client.client.time") as mock_time:
            mock_time.time.return_value = 100.0
            assert client.now() == 100.25

    @pytest.mark.asyncio
    async def test_stream(self, mock_response, client, mock_sleep, captured):
        mock_response.get(f"{URL}/clock", status=200, payload={"time": 200.4})
        mock_response.get(
            f"{URL}/events",
            status=200,
            body=": comment\n"
            + sse("snapshot", {"devices": {"d1": DEVICE, "d2": DEVICE}})
            + sse("unknown", {})
            + "event: pulse\ndata: 1794761689\n\n"
            + sse("patch", {"devices": {"d1": {"tint": "#FFFFFF"}, "d2": None}}),
        )
        with patch("onyx_client.client.time") as mock_time:
            mock_time.time.side_effect = [100.0, 100.2]
            stream = client.stream()
            events = [await anext(stream) for _ in range(4)]
            await stream.aclose()
        assert isinstance(events[0], Snapshot)
        assert set(events[0].devices) == {"d1", "d2"}
        assert isinstance(events[1], Pulse)
        assert events[1].time == 1794761689
        assert isinstance(events[2], DeviceChanged)
        assert events[2].device.tint == "#FFFFFF"
        assert isinstance(events[3], DeviceRemoved)
        assert events[3].identifier == "d2"
        assert client.clock_offset == pytest.approx(100.3)
        mock_sleep.assert_not_called()

    @pytest.mark.asyncio
    async def test_stream_reconnects_with_resync(
        self, mock_response, client, mock_sleep
    ):
        mock_response.get(f"{URL}/clock", status=401, repeat=True)
        mock_response.get(
            f"{URL}/events",
            status=200,
            body=sse("snapshot", {"devices": {"d1": DEVICE}}),
        )
        mock_response.get(
            f"{URL}/events",
            status=200,
            body=sse("snapshot", {"devices": {"d1": {**DEVICE, "name": "Renamed"}}}),
        )
        stream = client.stream()
        events = [await anext(stream) for _ in range(4)]
        await stream.aclose()
        assert [type(event) for event in events] == [
            Snapshot,
            Resynced,
            Snapshot,
            DeviceChanged,
        ]
        assert events[1].reason == "stream closed"
        assert events[3].device.name == "Renamed"
        assert client.clock_offset == 0
        mock_sleep.assert_awaited_once_with(1)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "hang", [False, True], ids=["request-timeout", "clock-stall"]
    )
    async def test_stream_clock_timeout(self, mock_response, client, hang, caplog):
        """A clock that does not answer must not delay or break the stream."""
        client.clock_offset = 1.5
        if hang:

            async def never():
                await asyncio.Event().wait()

            client.date_information = never
        else:
            mock_response.get(f"{URL}/clock", exception=TimeoutError())
        mock_response.get(
            f"{URL}/events",
            status=200,
            body=sse("snapshot", {"devices": {"d1": DEVICE}}),
        )
        with patch("onyx_client.client.CLOCK_TIMEOUT", 0.01):
            stream = client.stream()
            event = await asyncio.wait_for(anext(stream), 5)
            await stream.aclose()
        assert isinstance(event, Snapshot)
        assert client.clock_offset == 1.5
        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 1
        assert "timed out (TimeoutError), keeping the offset" in warnings[0].message

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "kwargs",
        [
            {"body": "not json", "content_type": "application/json"},
            {"payload": ["a"]},
            {"payload": "text"},
            {"payload": {"time": "abc"}},
            {"payload": {"time": [1]}},
        ],
        ids=["json", "list", "string", "bad-time", "list-time"],
    )
    async def test_stream_clock_invalid_data(
        self, mock_response, client, kwargs, caplog
    ):
        """A clock sending invalid data keeps the offset and connects."""
        client.clock_offset = 1.5
        mock_response.get(f"{URL}/clock", status=200, **kwargs)
        mock_response.get(f"{URL}/events", status=200, body=sse("snapshot", {}))
        stream = client.stream()
        event = await anext(stream)
        await stream.aclose()
        assert isinstance(event, Snapshot)
        assert client.clock_offset == 1.5
        assert "sent invalid data" in caplog.text

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "exception",
        [
            aiohttp.ClientConnectionError("down"),
            aiohttp.ServerDisconnectedError(),
            aiohttp.ConnectionTimeoutError(),
        ],
        ids=["connection", "disconnected", "connect-timeout"],
    )
    async def test_stream_clock_client_error(
        self, mock_response, client, exception, caplog
    ):
        client.clock_offset = 1.5
        mock_response.get(f"{URL}/clock", exception=exception)
        mock_response.get(f"{URL}/events", status=200, body=sse("snapshot", {}))
        stream = client.stream()
        event = await anext(stream)
        await stream.aclose()
        assert isinstance(event, Snapshot)
        assert client.clock_offset == 1.5
        assert "keeping the offset" in caplog.text

    @pytest.mark.asyncio
    async def test_stream_clock_response_error_is_best_effort(
        self, mock_response, client, caplog
    ):
        mock_response.get(
            f"{URL}/clock",
            exception=aiohttp.ClientResponseError(None, (), status=500, message="x"),
        )
        mock_response.get(f"{URL}/events", status=200, body=sse("snapshot", {}))
        stream = client.stream()
        event = await anext(stream)
        await stream.aclose()
        assert isinstance(event, Snapshot)
        assert "ClientResponseError status=500" in caplog.text

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status", [401, 403])
    async def test_stream_clock_rejected_credentials_raise(
        self, mock_response, client, status
    ):
        mock_response.get(
            f"{URL}/clock",
            exception=aiohttp.ClientResponseError(None, (), status=status),
        )
        with pytest.raises(aiohttp.ClientResponseError) as info:
            await anext(client.stream())
        assert info.value.status == status

    @pytest.mark.asyncio
    async def test_stream_cancel_during_clock(self, client, caplog):
        started = asyncio.Event()

        async def never():
            started.set()
            await asyncio.Event().wait()

        client.date_information = never
        task = asyncio.create_task(anext(client.stream()))
        await started.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert "ONYX clock" not in caplog.text

    @pytest.mark.asyncio
    async def test_stream_backoff(self, mock_response, client, mock_sleep):
        mock_response.get(f"{URL}/clock", status=200, payload={"time": 0}, repeat=True)
        mock_response.get(f"{URL}/events", status=500, repeat=True)
        mock_sleep.side_effect = [None] * 7 + [StopStream()]
        with pytest.raises(StopStream):
            async for _ in client.stream():
                pass
        assert [call.args[0] for call in mock_sleep.await_args_list] == [
            1,
            2,
            4,
            8,
            16,
            32,
            60,
            60,
        ]

    @pytest.mark.asyncio
    async def test_stream_reconnects_after_http_error(
        self, mock_response, client, mock_sleep
    ):
        mock_response.get(f"{URL}/clock", status=401, repeat=True)
        mock_response.get(f"{URL}/events", status=200, body=sse("snapshot", {}))
        mock_response.get(f"{URL}/events", status=500)
        mock_response.get(f"{URL}/events", status=200, body=sse("snapshot", {}))
        stream = client.stream()
        events = [await anext(stream) for _ in range(3)]
        await stream.aclose()
        assert isinstance(events[1], Resynced)
        assert "500" in events[1].reason

    @pytest.mark.asyncio
    async def test_stream_backoff_resets(self, mock_response, client, mock_sleep):
        mock_response.get(f"{URL}/clock", status=401, repeat=True)
        mock_response.get(f"{URL}/events", status=500)
        mock_response.get(f"{URL}/events", status=200, body=sse("snapshot", {}))
        mock_response.get(f"{URL}/events", status=500, repeat=True)
        mock_sleep.side_effect = [None, None, StopStream()]
        with pytest.raises(StopStream):
            async for _ in client.stream():
                pass
        assert [call.args[0] for call in mock_sleep.await_args_list] == [1, 1, 2]

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "body",
        [
            "event: snapshot\ndata: {\n\n",
            sse("patch", {"devices": {}}),
            "event: pulse\ndata: now\n\n",
            sse("snapshot", {"devices": {"d1": "broken"}}),
        ],
    )
    async def test_stream_reconnects_on_invalid_data(
        self, mock_response, client, mock_sleep, body
    ):
        mock_response.get(f"{URL}/clock", status=401, repeat=True)
        mock_response.get(f"{URL}/events", status=200, body=body)
        mock_response.get(f"{URL}/events", status=200, body=sse("snapshot", {}))
        stream = client.stream()
        event = await anext(stream)
        await stream.aclose()
        assert isinstance(event, Snapshot)
        mock_sleep.assert_awaited_once_with(1)

    @pytest.mark.asyncio
    async def test_resync(self, mock_response, client, mock_sleep):
        mock_response.get(f"{URL}/clock", status=401, repeat=True)
        mock_response.get(
            f"{URL}/events",
            status=200,
            body=sse("snapshot", {"devices": {"d1": DEVICE}}),
        )
        mock_response.get(
            f"{URL}/events",
            status=200,
            body=sse("snapshot", {"devices": {"d1": DEVICE}}),
        )
        stream = client.stream()
        assert isinstance(await anext(stream), Snapshot)
        client.resync()
        resynced = await anext(stream)
        assert isinstance(await anext(stream), Snapshot)
        await stream.aclose()
        assert isinstance(resynced, Resynced)
        assert resynced.reason == "resync requested"
        assert not client._resync_requested
        mock_sleep.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status", [401, 403])
    async def test_stream_unauthorized(self, mock_response, client, mock_sleep, status):
        mock_response.get(f"{URL}/clock", status=401)
        mock_response.get(f"{URL}/events", status=status)
        with pytest.raises(aiohttp.ClientResponseError):
            async for _ in client.stream():
                pass
        mock_sleep.assert_not_called()

    @pytest.mark.asyncio
    async def test_stream_timeout(self, mock_response, client, mock_sleep):
        mock_response.get(f"{URL}/clock", status=401, repeat=True)
        mock_response.get(f"{URL}/events", exception=aiohttp.ServerTimeoutError())
        mock_response.get(f"{URL}/events", status=200, body=sse("snapshot", {}))
        stream = client.stream()
        assert isinstance(await anext(stream), Snapshot)
        await stream.aclose()
        mock_sleep.assert_awaited_once_with(1)

    @pytest.mark.asyncio
    async def test_stream_patch_before_snapshot_after_reconnect(
        self, mock_response, client, mock_sleep
    ):
        mock_response.get(f"{URL}/clock", status=401, repeat=True)
        mock_response.get(
            f"{URL}/events",
            status=200,
            body=sse("snapshot", {"devices": {"d1": DEVICE}}),
        )
        mock_response.get(
            f"{URL}/events", status=200, body=sse("patch", {"devices": {"d1": None}})
        )
        mock_response.get(
            f"{URL}/events",
            status=200,
            body=sse("snapshot", {"devices": {"d1": DEVICE}}),
        )
        stream = client.stream()
        events = [await anext(stream) for _ in range(3)]
        await stream.aclose()
        assert [type(event) for event in events] == [Snapshot, Resynced, Snapshot]
        assert "PATCH_BEFORE_SNAPSHOT" in events[1].reason
        assert [call.args[0] for call in mock_sleep.await_args_list] == [1, 2]

    @pytest.mark.asyncio
    async def test_stream_close(self, mock_response, client, mock_sleep):
        mock_response.get(f"{URL}/clock", status=401, repeat=True)
        mock_response.get(
            f"{URL}/events",
            status=200,
            body=sse("snapshot", {}) + sse("snapshot", {}),
        )
        events = []
        async for event in client.stream():
            events.append(event)
            await client.close()
        assert len(events) == 1
        mock_sleep.assert_not_called()

    @pytest.mark.asyncio
    async def test_stream_closed_before_iteration(self, client):
        stream = client.stream()
        await client.close()
        assert [event async for event in stream] == []

    @pytest.mark.asyncio
    async def test_stream_ignores_clock_without_time(
        self, mock_response, client, mock_sleep
    ):
        mock_response.get(f"{URL}/clock", status=200, payload={})
        mock_response.get(f"{URL}/events", status=200, body=sse("snapshot", {}))
        stream = client.stream()
        await anext(stream)
        await stream.aclose()
        assert client.clock_offset == 0

    @pytest.mark.asyncio
    async def test_stream_aclose_releases_connection(self, mock_response, client):
        mock_response.get(f"{URL}/clock", status=401)
        mock_response.get(
            f"{URL}/events", status=200, body=sse("snapshot", {}) + sse("snapshot", {})
        )
        stream = client.stream()
        await anext(stream)
        response = client.url_helper._stream_response
        await stream.aclose()
        assert response.closed
        assert client.url_helper._stream_response is None

    @pytest.mark.asyncio
    async def test_resync_before_connected(self, mock_response, client, mock_sleep):
        async def resync_during_clock(*args, **kwargs):
            client.resync()

        mock_response.get(f"{URL}/clock", status=401, callback=resync_during_clock)
        mock_response.get(f"{URL}/clock", status=401)
        mock_response.get(f"{URL}/events", status=200, body=sse("snapshot", {}))
        mock_response.get(f"{URL}/events", status=200, body=sse("snapshot", {}))
        stream = client.stream()
        event = await anext(stream)
        await stream.aclose()
        assert isinstance(event, Snapshot)
        assert len(mock_response.requests[("GET", URL_EVENTS)]) == 2
        mock_sleep.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_context_manager(self, session):
        async with OnyxClient(Configuration("finger", "token"), session) as client:
            assert isinstance(client, OnyxClient)
        assert not session.closed

    @pytest.mark.asyncio
    async def test_close_owned_session(self):
        client = create(fingerprint="finger", access_token="token")
        session = client.client_session
        await client.close()
        assert session.closed

    @pytest.mark.asyncio
    async def test_close_unowned_session(self, session):
        client = OnyxClient(Configuration("finger", "token"), session)
        await client.close()
        assert not session.closed

    @pytest.mark.asyncio
    async def test_close_stream(self, client):
        with patch.object(client.url_helper, "close_stream") as close_stream:
            await client.close()
        close_stream.assert_called_once()
