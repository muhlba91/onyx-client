"""Tests for the mapper utils."""

import json

import pytest

from onyx_client.data.enum_value import EnumValue
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.click import Click
from onyx_client.device.device import Device
from onyx_client.device.input import Input
from onyx_client.device.light import Light
from onyx_client.device.shutter import Shutter
from onyx_client.device.switch import Switch
from onyx_client.device.tag_sun import TagSun
from onyx_client.device.tag_temperature import TagTemperature
from onyx_client.device.weather import Weather
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType
from onyx_client.utils.mapper import init_device, init_group


def numeric(value: int, maximum: int = 100) -> dict:
    return {
        "type": "numeric",
        "minimum": 0,
        "maximum": maximum,
        "value": value,
        "readonly": True,
    }


def enumeration(value: str, values: list) -> dict:
    return {"type": "enumeration", "value": value, "values": values, "readonly": True}


class TestInitDevice:
    def test_captured_shutter(self, captured):
        identifier = "00000000-0000-4000-8000-000000000005"
        data = json.loads(captured(f"details/{identifier}.json"))
        device = init_device(identifier, data)
        assert isinstance(device, Shutter)
        assert device.identifier == identifier
        assert device.name == "Shutter 5"
        assert device.device_type == DeviceType.ROLLERSHUTTER
        assert device.raw_type == "rollershutter"
        assert device.tint == "#F3F3F4"
        assert device.device_mode.mode == DeviceType.ROLLERSHUTTER
        assert device.actions == [Action.CLOSE, Action.OPEN, Action.STOP, Action.WINK]
        assert device.target_position == NumericValue(100, 0, 100, False)
        assert device.target_angle == NumericValue(0, 0, 360, False)
        assert device.actual_position == NumericValue(100, 0, 100, True)
        assert device.actual_angle == NumericValue(0, 0, 360, True)
        assert device.system_state == EnumValue(
            "ok",
            ["collision", "collision_not_calibrated", "not_calibrated", "ok"],
            True,
        )
        assert device.temperature is None
        assert device.active_command is None

    def test_summary(self, captured):
        devices = json.loads(captured("devices-v6.json"))
        identifier = "00000000-0000-4000-8000-000000000001"
        device = init_device(identifier, devices[identifier])
        assert isinstance(device, Shutter)
        assert device.device_type == DeviceType.RAFFSTORE_90
        assert device.actions == []
        assert device.actual_position is None

    def test_active_command(self):
        device = init_device(
            "id",
            {
                "type": "rollershutter",
                "active_command": {"source": {"name": "App User"}, "action": "open"},
            },
        )
        assert device.active_command.source.name == "App User"
        assert device.active_command.action == Action.OPEN

    def test_device_mode(self):
        device = init_device(
            "id",
            {
                "type": "rollershutter",
                "properties": {
                    "device_type": enumeration(
                        "awning", ["awning", "raffstore_90", "rollershutter"]
                    )
                },
            },
        )
        assert device.device_type == DeviceType.ROLLERSHUTTER
        assert device.device_mode.mode == DeviceType.AWNING
        assert device.device_mode.values == [
            DeviceType.AWNING,
            DeviceType.RAFFSTORE_90,
            DeviceType.ROLLERSHUTTER,
        ]

    def test_pergola(self):
        device = init_device(
            "id",
            {
                "type": "screen",
                "properties": {
                    "temperature": numeric(215, 850),
                    "humidity": numeric(40),
                },
            },
        )
        assert isinstance(device, Shutter)
        assert device.temperature.value == 215
        assert device.humidity.value == 40

    def test_rgbw_light(self):
        device = init_device(
            "id",
            {
                "type": "rgbw_light",
                "actions": ["light_on", "light_off"],
                "properties": {
                    "target_brightness": numeric(100, 65535),
                    "actual_brightness": numeric(50, 65535),
                    "dim_duration": numeric(5000, 3600000),
                    "target_hue": numeric(120, 359),
                    "actual_hue": numeric(110, 359),
                    "target_saturation": numeric(80),
                    "actual_saturation": numeric(70),
                    "target_color_temperature": numeric(4000, 10500),
                    "actual_color_temperature": numeric(3000, 10500),
                    "color_mode": enumeration("hsv", ["hsv", "temperature"]),
                },
            },
        )
        assert isinstance(device, Light)
        assert device.actions == [Action.LIGHT_ON, Action.LIGHT_OFF]
        assert device.target_brightness.value == 100
        assert device.actual_brightness.value == 50
        assert device.dim_duration.value == 5000
        assert device.target_hue.value == 120
        assert device.actual_hue.value == 110
        assert device.target_saturation.value == 80
        assert device.actual_saturation.value == 70
        assert device.target_color_temperature.value == 4000
        assert device.actual_color_temperature.value == 3000
        assert device.color_mode.value == "hsv"

    def test_weather(self):
        keys = [
            "wind_peak",
            "sun_brightness_peak",
            "sun_brightness_sink",
            "air_pressure",
            "humidity",
            "temperature",
            "wind_speed",
            "sun_brightness",
        ]
        device = init_device(
            "id",
            {
                "type": "weather",
                "properties": {key: numeric(i) for i, key in enumerate(keys)},
            },
        )
        assert isinstance(device, Weather)
        assert [getattr(device, key).value for key in keys] == list(range(len(keys)))

    def test_tag_sun(self):
        keys = ["sun_brightness", "sun_brightness_peak", "sun_brightness_sink"]
        device = init_device(
            "id",
            {
                "type": "tag_sun",
                "properties": {key: numeric(i) for i, key in enumerate(keys)},
            },
        )
        assert isinstance(device, TagSun)
        assert [getattr(device, key).value for key in keys] == [0, 1, 2]

    def test_tag_temperature(self):
        device = init_device(
            "id",
            {
                "type": "tag_temperature",
                "properties": {"temperature": numeric(215), "humidity": numeric(40)},
            },
        )
        assert isinstance(device, TagTemperature)
        assert device.temperature.value == 215
        assert device.humidity.value == 40

    def test_input(self):
        device = init_device(
            "id",
            {
                "type": "input",
                "properties": {
                    "input_type": enumeration("rain_sensor", ["rain_sensor"]),
                    "input_active": enumeration("true", ["true", "false"]),
                },
            },
        )
        assert isinstance(device, Input)
        assert device.input_type.value == "rain_sensor"
        assert device.input_active.as_bool()

    @pytest.mark.parametrize(
        ("offline", "expected"), [({}, True), ({"offline": False}, False)]
    )
    def test_click(self, offline, expected):
        device = init_device("id", {"type": "click", **offline})
        assert isinstance(device, Click)
        assert device.offline == expected

    def test_switch(self):
        assert isinstance(init_device("id", {"type": "switch"}), Switch)

    def test_unknown_type(self):
        device = init_device(
            "id",
            {"name": "name", "type": "future_device", "properties": {"x": numeric(1)}},
        )
        assert type(device) is Device
        assert device.device_type == DeviceType.UNKNOWN
        assert device.raw_type == "future_device"
        assert device.device_mode.mode == DeviceType.UNKNOWN

    @pytest.mark.parametrize(
        "raw_type",
        [
            "rollershutter",
            "rgbw_light",
            "weather",
            "tag_sun",
            "tag_temperature",
            "input",
            "click",
            "switch",
            "future_device",
        ],
    )
    def test_common_attributes(self, raw_type):
        device = init_device(
            "id",
            {
                "type": raw_type,
                "tint": "#FFFFFF",
                "actions": ["wink"],
                "active_command": {"action": "wink"},
            },
        )
        assert device.raw_type == raw_type
        assert device.tint == "#FFFFFF"
        assert device.actions == [Action.WINK]
        assert device.device_mode.mode == device.device_type
        assert device.active_command.action == Action.WINK

    def test_nulls(self):
        device = init_device(
            "id",
            {
                "type": "rollershutter",
                "actions": None,
                "properties": {
                    "device_type": {"value": "awning", "values": None},
                    "system_state": {"value": "ok", "values": None},
                },
                "active_command": {"attributes": None, "active_indicators": None},
            },
        )
        assert device.actions == []
        assert device.device_mode.values == []
        assert device.system_state.values == []
        assert device.active_command.attributes == []
        assert device.active_command.active_indicators == []
        assert init_group("id", {"devices": None}).devices == []

    def test_no_type(self):
        device = init_device("id", {})
        assert type(device) is Device
        assert device.device_type == DeviceType.UNKNOWN
        assert device.raw_type is None
        assert device.name is None
        assert device.actions == []


class TestInitGroup:
    def test_init_group(self, captured):
        groups = json.loads(captured("groups-v6.json"))
        identifier = "00000000-0000-4000-9000-000000000003"
        group = init_group(identifier, groups[identifier])
        assert group.identifier == identifier
        assert group.name == "Group 3"
        assert len(group.devices) == 3

    def test_init_group_empty(self):
        group = init_group("id", {})
        assert group.name is None
        assert group.devices == []
