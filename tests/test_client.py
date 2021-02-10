"""Tests for the Onyx Client."""
from unittest.mock import patch

import aiohttp
import pytest
from aioresponses import aioresponses

from onyx_client import Configuration, OnyxClient
from onyx_client.data.device_command import DeviceCommand
from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.device import Device
from onyx_client.device.shutter import Shutter
from onyx_client.device.weather import Weather
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType
from onyx_client.utils.const import API_HEADERS, API_URL, API_VERSION


class TestOnyxClient:
    @pytest.fixture
    async def session(self) -> aiohttp.ClientSession:
        sess = aiohttp.ClientSession()
        yield sess
        await sess.close()

    @pytest.fixture
    def mock_response(self):
        with aioresponses() as mocked:
            yield mocked

    @pytest.fixture
    def client(self, session) -> OnyxClient:
        yield OnyxClient(Configuration("finger", "token"), session)

    def test_headers(self, client):
        headers = client._headers
        for header in API_HEADERS:
            assert header in headers
        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer token"

    def test_base_url(self, client):
        assert client._base_url() == f"{API_URL}/box/finger/api/{API_VERSION}"

    def test_base_url_without_version(self, client):
        assert client._base_url(with_api=False) == f"{API_URL}/box/finger/api"

    def test_url(self, client):
        assert client._url("/path") == f"{API_URL}/box/finger/api/{API_VERSION}/path"

    def test_url_without_version(self, client):
        assert client._url("/path", with_api=False) == f"{API_URL}/box/finger/api/path"

    @patch("aiohttp.ClientResponse")
    def test_check_response(self, mock_response):
        mock_response.status = 200
        assert OnyxClient._check_response(mock_response)

    @patch("aiohttp.ClientResponse")
    def test_check_response_error(self, mock_response):
        mock_response.status = 401
        assert not OnyxClient._check_response(mock_response)

    def test_init_device_weather(self):
        device = OnyxClient._init_device("id", "name", DeviceType.WEATHER)
        assert isinstance(device, Device)
        assert device.identifier == "id"
        assert device.device_mode.mode == DeviceType.WEATHER
        assert device.device_mode.values is None

    def test_init_device_weather_full(self):
        device = OnyxClient._init_device(
            "id",
            "name",
            DeviceType.WEATHER,
            {
                "device_type": {
                    "type": "weather",
                    "values": ["weather"],
                },
                "wind_peak": {"value": 1, "minimum": 10},
                "sun_brightness_peak": {"value": 2, "minimum": 1, "maximum": 10},
                "sun_brightness_sink": {"value": 3, "minimum": 1, "maximum": 10},
                "air_pressure": {"value": 4, "minimum": 1, "maximum": 10},
                "humidity": {"value": 5, "minimum": 1, "maximum": 10},
                "temperature": {"value": 6, "minimum": 1, "maximum": 10},
            },
            list(Action),
        )
        assert isinstance(device, Weather)
        assert device.identifier == "id"
        assert device.device_mode.mode == DeviceType.WEATHER
        assert len(device.device_mode.values) == 1
        assert device.wind_peak == NumericValue(1, 10, 100, False)
        assert device.sun_brightness_peak == NumericValue(2, 1, 10, False)
        assert device.sun_brightness_sink == NumericValue(3, 1, 10, False)
        assert device.air_pressure == NumericValue(4, 1, 10, False)
        assert device.humidity == NumericValue(5, 1, 10, False)
        assert device.temperature == NumericValue(6, 1, 10, False)
        assert device.actions == list(Action)

    def test_init_device_shutter(self):
        device = OnyxClient._init_device("id", "name", DeviceType.AWNING)
        assert isinstance(device, Shutter)
        assert device.identifier == "id"
        assert device.device_mode.mode == DeviceType.AWNING
        assert device.device_mode.values is None

    def test_init_device_shutter_full(self):
        device = OnyxClient._init_device(
            "id",
            "name",
            DeviceType.AWNING,
            {
                "device_type": {
                    "type": "rollershutter",
                    "values": ["awning", "rollershutter"],
                },
                "target_position": {"value": 10, "minimum": 10},
                "target_angle": {"value": 1, "minimum": 1, "maximum": 10},
                "actual_position": {"value": 10, "minimum": 10},
                "actual_angle": {"value": 1, "minimum": 1, "maximum": 10},
                "drivetime_down": {
                    "maximum": 3600000,
                    "type": "numeric",
                    "value": 34031,
                },
                "drivetime_up": {
                    "maximum": 3600000,
                    "value": 34031,
                    "type": "numeric",
                },
                "rotationtime": {"maximum": 40000, "type": "numeric", "value": 5000},
            },
            list(Action),
        )
        assert isinstance(device, Shutter)
        assert device.identifier == "id"
        assert device.device_mode.mode == DeviceType.ROLLERSHUTTER
        assert len(device.device_mode.values) == 2
        assert device.target_position == NumericValue(10, 10, 100, False)
        assert device.target_angle == NumericValue(1, 1, 10, False)
        assert device.actions == list(Action)

    def test_init_device_unknown(self):
        device = OnyxClient._init_device(
            "id",
            "name",
            DeviceType.UNKNOWN,
        )
        assert isinstance(device, Device)
        assert device.identifier == "id"
        assert device.device_type == DeviceType.UNKNOWN
        assert device.device_mode.mode == DeviceType.UNKNOWN

    @pytest.mark.asyncio
    async def test_authorize(self, mock_response, session):
        mock_response.post(
            f"{API_URL}/authorize",
            status=200,
            payload={
                "fingerprint": "finger",
                "token": "token",
            },
        )
        config = await OnyxClient.authorize("code", session)
        assert isinstance(config, Configuration)
        assert config.fingerprint == "finger"
        assert config.access_token == "token"

    @pytest.mark.asyncio
    async def test_authorize_error(self, mock_response, session):
        mock_response.post(f"{API_URL}/authorize", status=401)
        auth = await OnyxClient.authorize("code", session)
        assert auth is None

    @pytest.mark.asyncio
    async def test_perform_get_request(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/path", status=200, payload={}
        )
        response = await client._perform_get_request("/path")
        assert response is not None

    @pytest.mark.asyncio
    async def test_perform_get_request_error(self, mock_response, client):
        mock_response.get(f"{API_URL}/box/finger/api/{API_VERSION}/path", status=401)
        response = await client._perform_get_request("/path")
        assert response is None

    @pytest.mark.asyncio
    async def test_perform_delete_request(self, mock_response, client):
        mock_response.delete(
            f"{API_URL}/box/finger/api/{API_VERSION}/path", status=200, payload={}
        )
        response = await client._perform_delete_request("/path")
        assert response is not None

    @pytest.mark.asyncio
    async def test_perform_delete_request_error(self, mock_response, client):
        mock_response.delete(f"{API_URL}/box/finger/api/{API_VERSION}/path", status=401)
        response = await client._perform_delete_request("/path")
        assert response is None

    @pytest.mark.asyncio
    async def test_perform_post_request(self, mock_response, client):
        mock_response.post(
            f"{API_URL}/box/finger/api/{API_VERSION}/path", status=200, payload={}
        )
        response = await client._perform_post_request("/path", {})
        assert response is not None

    @pytest.mark.asyncio
    async def test_perform_post_request_error(self, mock_response, client):
        mock_response.post(f"{API_URL}/box/finger/api/{API_VERSION}/path", status=401)
        response = await client._perform_post_request("/path", {})
        assert response is None

    @pytest.mark.asyncio
    async def test_verify(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/versions",
            status=200,
            payload={"versions": [API_VERSION, "v2"]},
        )
        assert await client.verify()

    @pytest.mark.asyncio
    async def test_verify_unknown_api_version(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/versions",
            status=200,
            payload={"versions": ["v1"]},
        )
        assert not await client.verify()

    @pytest.mark.asyncio
    async def test_verify_error(self, mock_response, client):
        mock_response.get(f"{API_URL}/box/finger/api/versions", status=401)
        assert not await client.verify()

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
    async def test_date_information_error(self, mock_response, client):
        mock_response.get(f"{API_URL}/box/finger/api/{API_VERSION}/clock", status=401)
        date = await client.date_information()
        assert date is None

    @pytest.mark.asyncio
    async def test_devices(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices",
            status=200,
            payload={
                "device1": {"name": "device1", "type": "rollershutter"},
                "device2": {"name": "device2", "type": "weather"},
            },
        )
        devices = await client.devices()
        assert devices is not None
        assert len(devices) == 2
        devices1 = list(filter(lambda dev: dev.identifier == "device1", devices))
        assert len(devices1) == 1
        device1 = devices1[0]
        assert device1 is not None
        assert isinstance(device1, Shutter)
        assert device1.name == "device1"
        devices2 = list(filter(lambda dev: dev.identifier == "device2", devices))
        assert len(devices2) == 1
        device2 = devices2[0]
        assert device2 is not None
        assert isinstance(device2, Device)
        assert device2.name == "device2"

    @patch("onyx_client.client.OnyxClient.device")
    @pytest.mark.asyncio
    async def test_devices_all_details(self, mock_device, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices",
            status=200,
            payload={
                "device1": {"name": "device1", "type": "rollershutter"},
                "device2": {"name": "device2", "type": "weather"},
            },
        )
        mock_device.return_value = Device(
            "id",
            "name",
            DeviceType.AWNING,
            DeviceMode(DeviceType.ROLLERSHUTTER),
            list(Action),
        )
        devices = await client.devices(True)
        assert mock_device.called
        assert devices is not None
        assert len(devices) == 2

    @pytest.mark.asyncio
    async def test_devices_error(self, mock_response, client):
        mock_response.get(f"{API_URL}/box/finger/api/{API_VERSION}/devices", status=401)
        devices = await client.devices()
        assert devices is None

    @pytest.mark.asyncio
    async def test_device_shutter(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device",
            status=200,
            payload={
                "name": "device",
                "type": "rollershutter",
                "properties": {
                    "device_type": {
                        "type": "awning",
                        "values": ["awning", "rollershutter"],
                    },
                    "target_position": {
                        "maximum": 100,
                        "value": 100,
                        "type": "numeric",
                    },
                    "target_angle": {"maximum": 360, "type": "numeric", "value": 0},
                    "actual_position": {
                        "maximum": 100,
                        "value": 100,
                        "type": "numeric",
                    },
                    "actual_angle": {"maximum": 360, "type": "numeric", "value": 0},
                    "drivetime_down": {
                        "maximum": 3600000,
                        "type": "numeric",
                        "value": 34031,
                    },
                    "drivetime_up": {
                        "maximum": 3600000,
                        "value": 34031,
                        "type": "numeric",
                    },
                    "rotationtime": {
                        "maximum": 40000,
                        "type": "numeric",
                        "value": 5000,
                    },
                },
                "actions": ["stop"],
            },
        )
        device = await client.device("device")
        assert isinstance(device, Shutter)
        assert device.device_type == DeviceType.ROLLERSHUTTER
        assert device.device_mode.mode == DeviceType.AWNING
        assert device.device_mode.values == [
            DeviceType.AWNING,
            DeviceType.ROLLERSHUTTER,
        ]
        assert device.actions == [Action.STOP]
        assert device.target_position == NumericValue(100, 0, 100, False)
        assert device.target_angle == NumericValue(0, 0, 360, False)

    @pytest.mark.asyncio
    async def test_device_weather(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device",
            status=200,
            payload={
                "name": "device",
                "type": "weather",
                "properties": {
                    "device_type": {
                        "type": "weather",
                        "values": ["weather"],
                    },
                    "wind_peak": {"value": 1, "minimum": 10},
                    "sun_brightness_peak": {"value": 2, "minimum": 1, "maximum": 10},
                    "sun_brightness_sink": {"value": 3, "minimum": 1, "maximum": 10},
                    "air_pressure": {"value": 4, "minimum": 1, "maximum": 10},
                    "humidity": {"value": 5, "minimum": 1, "maximum": 10},
                    "temperature": {"value": 6, "minimum": 1, "maximum": 10},
                },
                "actions": ["stop"],
            },
        )
        device = await client.device("device")
        assert isinstance(device, Weather)
        assert device.device_type == DeviceType.WEATHER
        assert device.device_mode.mode == DeviceType.WEATHER
        assert device.device_mode.values == [DeviceType.WEATHER]
        assert device.actions == [Action.STOP]
        assert device.wind_peak is not None
        assert device.sun_brightness_peak is not None
        assert device.sun_brightness_sink is not None
        assert device.air_pressure is not None
        assert device.humidity is not None
        assert device.temperature is not None

    @pytest.mark.asyncio
    async def test_device_error(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device", status=401
        )
        device = await client.device("device")
        assert device is None

    @pytest.mark.asyncio
    async def test_send_command(self, mock_response, client):
        mock_response.post(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device/command",
            status=200,
            payload={},
        )
        assert await client.send_command("device", DeviceCommand(action=Action.STOP))

    @pytest.mark.asyncio
    async def test_send_command_error(self, mock_response, client):
        mock_response.post(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device/command", status=401
        )
        assert not await client.send_command(
            "device", DeviceCommand(action=Action.STOP)
        )

    @pytest.mark.asyncio
    async def test_cancel_command(self, mock_response, client):
        mock_response.delete(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device/command",
            status=200,
            payload={},
        )
        assert await client.cancel_command("device")

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
        assert group1.name == "group1"
        assert group1.devices == ["device1"]
        groups2 = list(filter(lambda dev: dev.identifier == "group2", groups))
        assert len(groups2) == 1
        group2 = groups2[0]
        assert group2 is not None
        assert group2.name == "group2"
        assert group2.devices == ["device1", "device2"]

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
        assert group.name == "group"
        assert group.devices == ["device"]

    @pytest.mark.asyncio
    async def test_group_error(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups/group", status=401
        )
        group = await client.group("group")
        assert group is None

    @pytest.mark.asyncio
    async def test_send_group_command(self, mock_response, client):
        mock_response.post(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups/group/command",
            status=200,
            payload={"results": {"device": {"status_code": 200}}},
        )
        assert await client.send_group_command(
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
    async def test_send_group_command_error(self, mock_response, client):
        mock_response.post(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups/group/command", status=401
        )
        assert not await client.send_group_command(
            "group", DeviceCommand(action=Action.STOP)
        )

    @pytest.mark.asyncio
    async def test_cancel_group_command(self, mock_response, client):
        mock_response.delete(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups/group/command",
            status=200,
            payload={},
        )
        assert await client.cancel_group_command("group")

    @pytest.mark.asyncio
    async def test_cancel_group_command_error(self, mock_response, client):
        mock_response.delete(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups/group/command", status=401
        )
        assert not await client.cancel_group_command("group")
