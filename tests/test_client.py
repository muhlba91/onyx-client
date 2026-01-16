"""Tests for the Onyx Client."""

import aiohttp
import pytest
import pytest_asyncio
import asyncio

from unittest.mock import patch
from aioresponses import aioresponses

from onyx_client.client import create, OnyxClient
from onyx_client.configuration.configuration import Configuration
from onyx_client.data.animation_keyframe import AnimationKeyframe
from onyx_client.data.animation_value import AnimationValue
from onyx_client.data.device_command import DeviceCommand
from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.click import Click
from onyx_client.device.device import Device
from onyx_client.device.light import Light
from onyx_client.device.shutter import Shutter
from onyx_client.device.switch import Switch
from onyx_client.device.weather import Weather
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType
from onyx_client.utils.const import API_URL, API_VERSION


@patch("aiohttp.ClientSession")
def test_create_client(mock_session):
    client = create(
        fingerprint="finger", access_token="token", client_session=mock_session
    )
    assert client.url_helper.client_session == mock_session
    assert client.url_helper.config.fingerprint == "finger"
    assert client.url_helper.config.access_token == "token"
    assert client._shutdown
    assert client._read_loop_task is None
    assert client._event_loop is not None
    assert len(client._active_tasks) == 0
    assert client._event_callback is None


@patch("aiohttp.ClientSession")
def test_create_client_with_local_address(mock_session):
    client = create(
        fingerprint="finger",
        access_token="token",
        client_session=mock_session,
        local_address="192.168.1.1",
    )
    assert client.url_helper.client_session == mock_session
    assert client.url_helper.config.fingerprint == "finger"
    assert client.url_helper.config.access_token == "token"
    assert client.url_helper.config.local_address == "192.168.1.1"
    assert client._shutdown
    assert client._read_loop_task is None
    assert client._event_loop is not None
    assert len(client._active_tasks) == 0
    assert client._event_callback is None


@patch("aiohttp.ClientSession")
def test_create_client_with_config(mock_session):
    client = create(
        config=Configuration("finger", "token"), client_session=mock_session
    )
    assert client.url_helper.client_session == mock_session
    assert client.url_helper.config is not None
    assert client.url_helper.config.fingerprint == "finger"
    assert client.url_helper.config.access_token == "token"
    assert client.config is not None
    assert client.config.fingerprint == "finger"
    assert client.config.access_token == "token"
    assert client._shutdown
    assert client._read_loop_task is None
    assert client._event_loop is not None
    assert len(client._active_tasks) == 0
    assert client._event_callback is None


@patch("aiohttp.ClientSession")
def test_create_client_without_session(mock_session):
    client = create(fingerprint="finger", access_token="token")
    assert client.url_helper.client_session is not None
    assert client.url_helper.config.fingerprint == "finger"
    assert client.url_helper.config.access_token == "token"
    assert client.config.fingerprint == "finger"
    assert client.config.access_token == "token"
    assert client._shutdown
    assert client._read_loop_task is None
    assert client._event_loop is not None
    assert len(client._active_tasks) == 0
    assert client._event_callback is None


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
        yield OnyxClient(
            Configuration("finger", "token"), session, asyncio.get_event_loop()
        )

    def test_set_event_callback(self, client):
        callback = 0
        client.set_event_callback(callback)
        assert client._event_callback == callback

    def test__complete_internal_task(self, client):
        class Task:
            def cancelled(self):
                return True

        callback = Task()
        client._active_tasks.add(callback)
        assert len(client._active_tasks) == 1
        assert callback in client._active_tasks
        client._complete_internal_task(callback)
        assert len(client._active_tasks) == 0

    def test__complete_internal_task_cancelled(self, client):
        class Task:
            def cancelled(self):
                return False

            def exception(self):
                raise Exception("error")

        callback = Task()
        client._active_tasks.add(callback)
        assert len(client._active_tasks) == 1
        assert callback in client._active_tasks
        with pytest.raises(Exception):
            client._complete_internal_task(callback)
        assert len(client._active_tasks) == 0

    def test_stop(self, client):
        assert client._shutdown

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

    @patch("onyx_client.client.OnyxClient.device")
    @pytest.mark.asyncio
    async def test_devices_all_details_none(self, mock_device, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices",
            status=200,
            payload={
                "device1": {},
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
        assert len(devices) == 1

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
                        "minimum": 0,
                        "value": 100,
                        "type": "numeric",
                        "animation": {
                            "start": 1637499009.158352,
                            "current_value": 20,
                            "keyframes": [
                                {
                                    "interpolation": "linear",
                                    "delay": 0,
                                    "duration": 42.0273,
                                    "value": 90,
                                }
                            ],
                        },
                    },
                    "actual_angle": {
                        "maximum": 360,
                        "minimum": 0,
                        "type": "numeric",
                        "value": 0,
                        "animation": {
                            "start": 1637499108.0069883,
                            "current_value": 90,
                            "keyframes": [
                                {
                                    "interpolation": "linear",
                                    "delay": 0,
                                    "duration": 0.791666666,
                                    "value": 33,
                                }
                            ],
                        },
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
        assert device.target_position == NumericValue(100, None, 100, False)
        assert device.target_angle == NumericValue(0, None, 360, False)
        assert device.actual_position == NumericValue(
            100,
            0,
            100,
            False,
            AnimationValue(
                1637499009.158352, 20, [AnimationKeyframe("linear", 0, 42.0273, 90)]
            ),
        )
        assert device.actual_angle == NumericValue(
            0,
            0,
            360,
            False,
            AnimationValue(
                1637499108.0069883,
                90,
                [AnimationKeyframe("linear", 0, 0.791666666, 33)],
            ),
        )

    @pytest.mark.asyncio
    async def test_device_shutter_no_data(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device",
            status=200,
            payload={
                "type": "rollershutter",
            },
        )
        device = await client.device("device")
        assert isinstance(device, Shutter)
        assert device.device_type == DeviceType.ROLLERSHUTTER
        assert device.device_mode.mode == DeviceType.ROLLERSHUTTER
        assert device.device_mode.values is None
        assert len(device.actions) == 0
        assert device.target_position is None
        assert device.target_angle is None
        assert device.actual_position is None
        assert device.actual_angle is None

    @pytest.mark.asyncio
    async def test_device_pergola_awning_roof(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device",
            status=200,
            payload={
                "name": "device",
                "type": "pergola_awning_roof",
                "actions": ["close", "open", "stop", "wink"],
                "properties": {
                    "actual_angle": {
                        "type": "numeric",
                        "minimum": 0,
                        "maximum": 360,
                        "value": 0,
                        "readonly": True,
                    },
                    "actual_position": {
                        "type": "numeric",
                        "minimum": 0,
                        "maximum": 100,
                        "value": 100,
                        "readonly": True,
                    },
                    "system_state": {
                        "type": "enumeration",
                        "value": "ok",
                        "values": [
                            "collision",
                            "collision_not_calibrated",
                            "not_calibrated",
                            "ok",
                        ],
                        "readonly": True,
                    },
                    "target_angle": {
                        "type": "numeric",
                        "minimum": 0,
                        "maximum": 360,
                        "value": 0,
                        "readonly": False,
                    },
                    "target_position": {
                        "type": "numeric",
                        "minimum": 0,
                        "maximum": 100,
                        "value": 100,
                        "readonly": False,
                    },
                },
            },
        )
        device = await client.device("device")
        assert isinstance(device, Shutter)
        assert device.device_type == DeviceType.PERGOLA_AWNING_ROOF
        assert device.device_mode.mode is None
        assert len(device.device_mode.values) == 0
        assert device.actions == [Action.CLOSE, Action.OPEN, Action.STOP, Action.WINK]
        assert device.target_position == NumericValue(100, 0, 100, False)
        assert device.target_angle == NumericValue(0, 0, 360, False)
        assert device.actual_position == NumericValue(
            100,
            0,
            100,
            False,
        )
        assert device.actual_angle == NumericValue(
            0,
            0,
            360,
            False,
        )

    @pytest.mark.asyncio
    async def test_device_awning(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device",
            status=200,
            payload={
                "name": "device",
                "type": "awning",
                "actions": ["close", "open", "stop", "wink"],
                "properties": {
                    "actual_angle": {
                        "type": "numeric",
                        "minimum": 0,
                        "maximum": 360,
                        "value": 0,
                        "readonly": True,
                    },
                    "actual_position": {
                        "type": "numeric",
                        "minimum": 0,
                        "maximum": 100,
                        "value": 0,
                        "readonly": True,
                    },
                    "system_state": {
                        "type": "enumeration",
                        "value": "ok",
                        "values": [
                            "collision",
                            "collision_not_calibrated",
                            "not_calibrated",
                            "ok",
                        ],
                        "readonly": True,
                    },
                    "target_angle": {
                        "type": "numeric",
                        "minimum": 0,
                        "maximum": 360,
                        "value": 0,
                        "readonly": False,
                    },
                    "target_position": {
                        "type": "numeric",
                        "minimum": 0,
                        "maximum": 100,
                        "value": 0,
                        "readonly": False,
                    },
                },
            },
        )
        device = await client.device("device")
        assert isinstance(device, Shutter)
        assert device.device_type == DeviceType.AWNING
        assert device.device_mode.mode is None
        assert len(device.device_mode.values) == 0
        assert device.actions == [Action.CLOSE, Action.OPEN, Action.STOP, Action.WINK]
        assert device.target_position == NumericValue(0, 0, 100, False)
        assert device.target_angle == NumericValue(0, 0, 360, False)
        assert device.actual_position == NumericValue(
            0,
            0,
            100,
            False,
        )
        assert device.actual_angle == NumericValue(
            0,
            0,
            360,
            False,
        )

    @pytest.mark.asyncio
    async def test_device_weather(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device",
            status=200,
            payload={
                "name": "device",
                "type": "weather",
                "actions": ["wink"],
                "properties": {
                    "air_pressure": {
                        "type": "numeric",
                        "minimum": 0,
                        "maximum": 150000,
                        "value": 90374,
                        "readonly": True,
                    },
                    "humidity": {
                        "type": "numeric",
                        "minimum": 0,
                        "maximum": 100,
                        "value": 78,
                        "readonly": True,
                    },
                    "sun_brightness_peak": {
                        "type": "numeric",
                        "minimum": 0,
                        "maximum": 150000,
                        "value": 53710,
                        "readonly": True,
                    },
                    "sun_brightness_sink": {
                        "type": "numeric",
                        "minimum": 0,
                        "maximum": 150001,
                        "value": 20966,
                        "readonly": True,
                    },
                    "temperature": {
                        "type": "numeric",
                        "minimum": -400,
                        "maximum": 1500,
                        "value": 72,
                        "readonly": True,
                    },
                    "wind_peak": {
                        "type": "numeric",
                        "minimum": 0,
                        "maximum": 100000,
                        "value": 2501,
                        "readonly": True,
                    },
                },
            },
        )
        device = await client.device("device")
        assert isinstance(device, Weather)
        assert device.device_type == DeviceType.WEATHER
        assert device.device_mode.mode is None
        assert device.device_mode.values == []
        assert device.actions == [Action.WINK]
        assert device.wind_peak is not None
        assert device.wind_peak.minimum == 0
        assert device.wind_peak.maximum == 100000
        assert device.wind_peak.value == 2501
        assert device.sun_brightness_peak is not None
        assert device.sun_brightness_peak.minimum == 0
        assert device.sun_brightness_peak.maximum == 150000
        assert device.sun_brightness_peak.value == 53710
        assert device.sun_brightness_sink is not None
        assert device.sun_brightness_sink.minimum == 0
        assert device.sun_brightness_sink.maximum == 150001
        assert device.sun_brightness_sink.value == 20966
        assert device.air_pressure is not None
        assert device.air_pressure.minimum == 0
        assert device.air_pressure.maximum == 150000
        assert device.air_pressure.value == 90374
        assert device.humidity is not None
        assert device.humidity.minimum == 0
        assert device.humidity.maximum == 100
        assert device.humidity.value == 78
        assert device.temperature is not None
        assert device.temperature.minimum == -400
        assert device.temperature.maximum == 1500
        assert device.temperature.value == 72

    @pytest.mark.asyncio
    async def test_device_weather_no_data(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device",
            status=200,
            payload={
                "type": "weather",
            },
        )
        device = await client.device("device")
        assert isinstance(device, Weather)
        assert device.device_type == DeviceType.WEATHER
        assert device.device_mode.mode == DeviceType.WEATHER
        assert device.device_mode.values is None
        assert len(device.actions) == 0
        assert device.wind_peak is None
        assert device.sun_brightness_peak is None
        assert device.sun_brightness_sink is None
        assert device.air_pressure is None
        assert device.humidity is None
        assert device.temperature is None

    @pytest.mark.asyncio
    async def test_device_light(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device",
            status=200,
            payload={
                "name": "device",
                "type": "basic_light",
                "properties": {
                    "device_type": {
                        "type": "basic_light",
                        "values": ["basic_light"],
                    },
                    "target_brightness": {"value": 1, "minimum": 10},
                    "actual_brightness": {"value": 2, "minimum": 1, "maximum": 10},
                    "dim_duration": {"value": 3, "minimum": 1, "maximum": 10},
                },
                "actions": ["stop"],
            },
        )
        device = await client.device("device")
        assert isinstance(device, Light)
        assert device.device_type == DeviceType.BASIC_LIGHT
        assert device.device_mode.mode == DeviceType.BASIC_LIGHT
        assert device.device_mode.values == [DeviceType.BASIC_LIGHT]
        assert device.actions == [Action.STOP]
        assert device.target_brightness is not None
        assert device.actual_brightness is not None
        assert device.dim_duration is not None

    @pytest.mark.asyncio
    async def test_device_light_no_data(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device",
            status=200,
            payload={
                "type": "basic_light",
            },
        )
        device = await client.device("device")
        assert isinstance(device, Light)
        assert device.device_type == DeviceType.BASIC_LIGHT
        assert device.device_mode.mode == DeviceType.BASIC_LIGHT
        assert device.device_mode.values is None
        assert len(device.actions) == 0
        assert device.target_brightness is None
        assert device.actual_brightness is None
        assert device.dim_duration is None

    @pytest.mark.asyncio
    async def test_device_dimmable_light(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device",
            status=200,
            payload={
                "name": "device",
                "type": "dimmable_light",
                "properties": {
                    "target_brightness": {"value": 1, "minimum": 10},
                    "actual_brightness": {"value": 2, "minimum": 1, "maximum": 10},
                    "dim_duration": {"value": 3, "minimum": 1, "maximum": 10},
                },
                "actions": ["stop"],
            },
        )
        device = await client.device("device")
        assert isinstance(device, Light)
        assert device.device_type == DeviceType.DIMMABLE_LIGHT
        assert device.device_mode.mode is None
        assert len(device.device_mode.values) == 0
        assert device.actions == [Action.STOP]
        assert device.target_brightness is not None
        assert device.actual_brightness is not None
        assert device.dim_duration is not None

    @pytest.mark.asyncio
    async def test_device_dimmable_light_animation(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device",
            status=200,
            payload={
                "name": "device",
                "type": "dimmable_light",
                "actions": ["light_off", "light_on", "stop", "wink"],
                "properties": {
                    "actual_brightness": {
                        "type": "numeric",
                        "minimum": 0,
                        "maximum": 65535,
                        "value": 33153,
                        "readonly": True,
                        "animation": {
                            "current_value": 0,
                            "keyframes": [
                                {
                                    "delay": 0,
                                    "duration": 0.267689021,
                                    "interpolation": "linear",
                                    "value": 35086,
                                }
                            ],
                            "start": 1702300612.2786393,
                        },
                    },
                    "dim_duration": {
                        "type": "numeric",
                        "minimum": 20,
                        "maximum": 3600000,
                        "value": 6000,
                        "readonly": False,
                    },
                    "target_brightness": {
                        "type": "numeric",
                        "minimum": 0,
                        "maximum": 65535,
                        "value": 33153,
                        "readonly": False,
                    },
                },
            },
        )
        device = await client.device("device")
        assert isinstance(device, Light)
        assert device.device_type == DeviceType.DIMMABLE_LIGHT
        assert device.device_mode.mode is None
        assert len(device.device_mode.values) == 0
        assert device.actions == [
            Action.LIGHT_OFF,
            Action.LIGHT_ON,
            Action.STOP,
            Action.WINK,
        ]
        assert device.target_brightness is not None
        assert device.actual_brightness is not None
        assert device.actual_brightness.animation is not None
        assert device.dim_duration is not None

    @pytest.mark.asyncio
    async def test_device_click(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device",
            status=200,
            payload={
                "type": "click",
                "offline": True,
            },
        )
        device = await client.device("device")
        assert isinstance(device, Click)
        assert device.device_type == DeviceType.CLICK
        assert device.device_mode.mode == DeviceType.CLICK
        assert device.device_mode.values is None
        assert len(device.actions) == 0
        assert device.offline

    @pytest.mark.asyncio
    async def test_device_click_no_data(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device",
            status=200,
            payload={
                "name": "device",
                "type": "click",
            },
        )
        device = await client.device("device")
        assert isinstance(device, Click)
        assert device.device_type == DeviceType.CLICK
        assert device.device_mode.mode == DeviceType.CLICK
        assert device.device_mode.values is None
        assert len(device.actions) == 0
        assert device.offline

    @pytest.mark.asyncio
    async def test_device_switch(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device",
            status=200,
            payload={
                "type": "switch",
            },
        )
        device = await client.device("device")
        assert isinstance(device, Switch)
        assert device.device_type == DeviceType.SWITCH
        assert device.device_mode.mode == DeviceType.SWITCH
        assert device.device_mode.values is None
        assert len(device.actions) == 0

    @pytest.mark.asyncio
    async def test_device_no_properties(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device",
            status=200,
            payload={
                "name": "device",
                "type": "rollershutter",
                "offline": True,
            },
        )
        device = await client.device("device")
        assert isinstance(device, Shutter)
        assert device.device_type == DeviceType.ROLLERSHUTTER
        assert device.device_mode.mode == DeviceType.ROLLERSHUTTER
        assert device.device_mode.values is None
        assert len(device.actions) == 0
        assert device.target_position is None
        assert device.target_angle is None
        assert device.actual_position is None
        assert device.actual_angle is None

    @pytest.mark.asyncio
    async def test_device_no_data(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/devices/device",
            status=200,
            payload={},
        )
        device = await client.device("device")
        assert isinstance(device, Device)
        assert device.device_type == DeviceType.UNKNOWN
        assert device.device_mode.mode is None
        assert device.device_mode.values is None
        assert len(device.actions) == 0

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
        mock_response.post(
            f"{API_URL}/box/finger/api/{API_VERSION}/groups/group/command",
            status=200,
            payload={"results": {"device": {"status_code": 200}}},
        )
        assert await client.send_group_command(
            "group", DeviceCommand(action=Action.STOP)
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

    @pytest.mark.asyncio
    async def test_events(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=200,
            body="event: pulse\n"
            "data: 1730803627\n\n"
            "event: snapshot\n"
            'data: { "devices": { "device1":'
            '{ "name": "device1", "type": "rollershutter" },'
            '"device2": { "name": "device2" },'
            '"device3": { "type": "rollershutter" } } }',
        )
        index = 1
        async for device in client.events():
            assert device.identifier == f"device{index}"
            index += 1
        assert index == 4

    @patch("onyx_client.client.OnyxClient._complete_internal_task")
    @pytest.mark.asyncio
    async def test_start(self, mock__complete_internal_task, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=200,
            body="event: pulse\n"
            "data: 1730803627\n\n"
            "event: snapshot\n"
            'data: { "devices": { "device1":'
            '{ "name": "device1", "type": "rollershutter" },'
            '"device2": { "name": "device2" },'
            '"device3": { "type": "rollershutter" } } }',
        )

        def callback(device):
            if device.identifier == "device3":
                client.stop()

        async def check_index(task):
            assert task in client._active_tasks
            assert client._shutdown
            assert len(client._active_tasks) == 0
            await task

        mock__complete_internal_task.side_effect = check_index
        client.set_event_callback(callback)
        client.start()
        assert len(client._active_tasks) == 1
        assert not client._shutdown
        for task in client._active_tasks.copy():
            await task

    @pytest.mark.asyncio
    async def test_start_break(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=200,
            body="event: pulse\n"
            "data: 1730803627\n\n"
            "event: snapshot\n"
            'data: { "devices": { "device1":'
            '{ "name": "device1", "type": "rollershutter" },'
            '"device2": { "name": "device2" },'
            '"device3": { "type": "rollershutter" } } }',
        )

        def callback(device):
            if device.identifier == "device1":
                client.stop()

        client.set_event_callback(callback)
        client.start()
        assert len(client._active_tasks) == 1
        assert not client._shutdown
        for task in client._active_tasks.copy():
            await task

    @pytest.mark.asyncio
    async def test_start_without_callback(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=200,
            body="event: pulse\n"
            "data: 1730803627\n\n"
            "event: snapshot\n"
            'data: { "devices": { "device1":'
            '{ "name": "device1", "type": "rollershutter" },'
            '"device2": { "name": "device2" },'
            '"device3": { "type": "rollershutter" } } }',
        )

        client.start()
        assert not client._shutdown
        assert len(client._active_tasks) == 1

    @patch("onyx_client.client.OnyxClient.device")
    @pytest.mark.asyncio
    async def test_events_details(self, mock_device, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=200,
            body="event: pulse\n"
            "data: 1730803627\n\n"
            "event: snapshot\n"
            'data: { "devices": { "device":'
            '{ "name": "device", "type": "rollershutter" } } }',
        )
        mock_device.return_value = Device(
            "id",
            "name",
            DeviceType.AWNING,
            DeviceMode(DeviceType.ROLLERSHUTTER),
            list(Action),
        )
        index = 1
        async for device in client.events(True):
            assert device.identifier == "id"
            index += 1
        assert index == 2
        assert mock_device.called

    @patch("onyx_client.client.OnyxClient.device")
    @pytest.mark.asyncio
    async def test_events_device_exception(self, mock_device, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=200,
            body="event: pulse\n"
            "data: 1730803627\n\n"
            "event: patch\n"
            'data: { "devices": { "device":'
            '{ "name": "device", "type": "rollershutter" } } }',
        )
        mock_device.side_effect = AttributeError()
        index = 1
        async for device in client.events(True):
            index += 1
        assert index == 1
        assert mock_device.called

    @pytest.mark.asyncio
    async def test_events_empty_data(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=200,
            body="event: pulse\n"
            "data: 1730803627\n\n"
            "event: patch\n"
            'data: { "devices": { "device1": {} } }',
        )
        index = 1
        async for device in client.events():
            assert device.identifier == f"device{index}"
            index += 1
        assert index == 2

    @pytest.mark.asyncio
    async def test_events_no_devices(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=200,
            body="event: pulse\n"
            "data: 1730803627\n\n"
            "event: patch\n"
            'data: { "devices": {  } }',
        )
        index = 1
        async for device in client.events():
            assert device.identifier == f"device{index}"
            index += 1
        assert index == 1

    @pytest.mark.asyncio
    async def test_events_none(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=200,
            body="event: pulse\ndata: 1730803627\n\nevent: patch\ndata: {  }",
        )
        index = 1
        async for device in client.events():
            index += 1
        assert index == 1

    @pytest.mark.asyncio
    async def test_events_error(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=500,
            body="event: pulse\ndata: 1730803627\n\nevent: patch\ndata: {  }",
        )
        index = 1
        async for device in client.events():
            index += 1
        assert index == 1

    @pytest.mark.asyncio
    async def test_events_shutter(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=200,
            body="event: pulse\n"
            "data: 1730803627\n\n"
            "event: patch\n"
            'data: { "devices": { "device1":'
            '{ "name": "device1", "type": "rollershutter" },'
            '"device2": { "name": "device2" },'
            '"device3": { "type": "rollershutter" } } }',
        )
        index = 1
        async for device in client.events():
            assert device.identifier == f"device{index}"
            index += 1
        assert index == 4

    @pytest.mark.asyncio
    async def test_events_multiple_pulses(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=200,
            body="event: pulse\n"
            "data: 1730803627\n\n"
            "event: pulse\n"
            "data: 1732886606\n\n"
            "event: patch\n"
            'data: { "devices": { "device1":'
            '{ "name": "device1", "type": "rollershutter" },'
            '"device2": { "name": "device2" },'
            '"device3": { "type": "rollershutter" } } }\n\n'
            "event: pulse\n"
            "data: 1730803627\n\n",
        )
        index = 1
        async for device in client.events():
            assert device.identifier == f"device{index}"
            index += 1
        assert index == 4

    @pytest.mark.asyncio
    async def test_events_invalid_orders(self, mock_response, client):
        mock_response.get(
            f"{API_URL}/box/finger/api/{API_VERSION}/events",
            status=200,
            body="event: pulse\n"
            "data: 1730803627\n\n"
            "data: 1732886606\n\n"
            "event: patch\n"
            "event: pulse\n"
            "data: 1730803627\n\n"
            "event: patch\n"
            'data: { "devices": { "device1":'
            '{ "name": "device1", "type": "rollershutter" },'
            '"device2": { "name": "device2" },'
            '"device3": { "type": "rollershutter" } } }\n\n'
            "event: pulse\n"
            "data: 1730803627\n\n",
        )
        index = 1
        async for device in client.events():
            assert device.identifier == f"device{index}"
            index += 1
        assert index == 4
