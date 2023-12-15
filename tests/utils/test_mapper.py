"""Tests for mapper utils."""
from onyx_client.data.boolean_value import BooleanValue
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.click import Click
from onyx_client.device.device import Device
from onyx_client.device.light import Light
from onyx_client.device.shutter import Shutter
from onyx_client.device.switch import Switch
from onyx_client.device.weather import Weather
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType
from onyx_client.utils.mapper import numeric_value, boolean_value, init_device


def test_numeric_value():
    assert numeric_value("key", {"key": {"value": 1}}) == NumericValue(
        value=1, minimum=None, maximum=None, read_only=False
    )


def test_numeric_value_full():
    assert numeric_value(
        "key", {"key": {"value": 1, "minimum": 0, "maximum": 10}}
    ) == NumericValue(value=1, minimum=0, maximum=10, read_only=False)


def test_numeric_value_empty_properties():
    assert numeric_value("key", {}) is None


def test_numeric_value_no_properties():
    assert numeric_value("key", None) is None


def test_boolean_value():
    assert boolean_value("key", {"key": {"value": "true"}}) == BooleanValue(
        value=True, read_only=False
    )


def test_boolean_value_empty_properties():
    assert boolean_value("key", {}) is None


def test_boolean_value_no_properties():
    assert boolean_value("key", None) is None


def test_init_device_click():
    device = init_device("id", "name", DeviceType.CLICK)
    assert isinstance(device, Click)
    assert device.identifier == "id"
    assert device.device_mode.mode == DeviceType.CLICK
    assert device.device_mode.values is None
    assert device.offline


def test_init_device_click_full():
    device = init_device(
        "id", "name", DeviceType.CLICK, None, list(Action), {"offline": False}
    )
    assert isinstance(device, Click)
    assert device.identifier == "id"
    assert device.device_mode.mode == DeviceType.CLICK
    assert device.device_mode.values is None
    assert not device.offline


def test_init_device_switch():
    device = init_device("id", "name", DeviceType.SWITCH)
    assert isinstance(device, Switch)
    assert device.identifier == "id"
    assert device.device_mode.mode == DeviceType.SWITCH
    assert device.device_mode.values is None


def test_init_device_switch_full():
    device = init_device("id", "name", DeviceType.CLICK, None, list(Action))
    assert isinstance(device, Click)
    assert device.identifier == "id"
    assert device.device_mode.mode == DeviceType.CLICK
    assert device.device_mode.values is None


def test_init_device_weather():
    device = init_device("id", "name", DeviceType.WEATHER)
    assert isinstance(device, Weather)
    assert device.identifier == "id"
    assert device.name == "name"
    assert device.device_mode.mode == DeviceType.WEATHER
    assert device.device_mode.values is None


def test_init_device_weather_minimal():
    device = init_device("id", None, DeviceType.WEATHER)
    assert isinstance(device, Weather)
    assert device.identifier == "id"
    assert device.name is None
    assert device.device_mode.mode == DeviceType.WEATHER
    assert device.device_mode.values is None


def test_init_device_weather_full():
    device = init_device(
        "id",
        "name",
        DeviceType.WEATHER,
        {
            "device_type": {
                "type": "weather",
                "values": ["weather"],
            },
            "wind_peak": {"value": 1, "minimum": 10},
            "sun_brightness_peak": {"value": 2, "minimum": 1},
            "sun_brightness_sink": {"minimum": 1, "maximum": 10},
            "air_pressure": {"value": 4, "minimum": 1, "maximum": 10},
            "humidity": {"value": 5, "minimum": 1, "maximum": 10},
            "temperature": {"value": 6, "minimum": 1, "maximum": 10},
        },
        list(Action),
    )
    assert isinstance(device, Weather)
    assert device.identifier == "id"
    assert device.name == "name"
    assert device.device_mode.mode == DeviceType.WEATHER
    assert len(device.device_mode.values) == 1
    assert device.wind_peak == NumericValue(1, 10, None, False)
    assert device.sun_brightness_peak == NumericValue(2, 1, None, False)
    assert device.sun_brightness_sink == NumericValue(None, 1, 10, False)
    assert device.air_pressure == NumericValue(4, 1, 10, False)
    assert device.humidity == NumericValue(5, 1, 10, False)
    assert device.temperature == NumericValue(6, 1, 10, False)
    assert device.actions == list(Action)


def test_init_device_weather_no_device_type():
    device = init_device(
        "id",
        "name",
        DeviceType.WEATHER,
        {
            "device_type": {},
        },
        list(Action),
    )
    assert isinstance(device, Weather)
    assert device.identifier == "id"
    assert device.name == "name"
    assert device.device_mode.mode is None
    assert len(device.device_mode.values) == 0


def test_init_device_light():
    device = init_device("id", "name", DeviceType.BASIC_LIGHT)
    assert isinstance(device, Light)
    assert device.identifier == "id"
    assert device.name == "name"
    assert device.device_mode.mode == DeviceType.BASIC_LIGHT
    assert device.device_mode.values is None


def test_init_device_light_minimal():
    device = init_device("id", None, DeviceType.BASIC_LIGHT)
    assert isinstance(device, Light)
    assert device.identifier == "id"
    assert device.name is None
    assert device.device_mode.mode == DeviceType.BASIC_LIGHT
    assert device.device_mode.values is None


def test_init_device_light_full():
    device = init_device(
        "id",
        "name",
        DeviceType.BASIC_LIGHT,
        {
            "device_type": {
                "type": "basic_light",
                "values": ["basic_light"],
            },
            "target_brightness": {"value": 1, "minimum": 10},
            "actual_brightness": {"value": 2, "maximum": 10},
            "dim_duration": {"minimum": 1, "maximum": 10},
        },
        list(Action),
    )
    assert isinstance(device, Light)
    assert device.identifier == "id"
    assert device.name == "name"
    assert device.device_mode.mode == DeviceType.BASIC_LIGHT
    assert len(device.device_mode.values) == 1
    assert device.target_brightness == NumericValue(1, 10, None, False)
    assert device.actual_brightness == NumericValue(2, None, 10, False)
    assert device.dim_duration == NumericValue(None, 1, 10, False)
    assert device.actions == list(Action)


def test_init_device_shutter():
    device = init_device("id", "name", DeviceType.AWNING)
    assert isinstance(device, Shutter)
    assert device.identifier == "id"
    assert device.name == "name"
    assert device.device_mode.mode == DeviceType.AWNING
    assert device.device_mode.values is None


def test_init_device_shutter_minimal():
    device = init_device("id", None, DeviceType.AWNING)
    assert isinstance(device, Shutter)
    assert device.identifier == "id"
    assert device.name is None
    assert device.device_mode.mode == DeviceType.AWNING
    assert device.device_mode.values is None


def test_init_device_shutter_full():
    device = init_device(
        "id",
        "name",
        DeviceType.AWNING,
        {
            "device_type": {
                "type": "rollershutter",
                "values": ["awning", "rollershutter"],
            },
            "target_position": {"value": 10, "minimum": 10},
            "target_angle": {"value": 1, "maximum": 10},
            "actual_position": {"minimum": 0, "maximum": 10},
            "actual_angle": {"value": 1, "minimum": 1, "maximum": 10},
        },
        list(Action),
    )
    assert isinstance(device, Shutter)
    assert device.identifier == "id"
    assert device.name == "name"
    assert device.device_mode.mode == DeviceType.ROLLERSHUTTER
    assert len(device.device_mode.values) == 2
    assert device.target_position == NumericValue(10, 10, None, False)
    assert device.target_angle == NumericValue(1, None, 10, False)
    assert device.actual_position == NumericValue(None, 0, 10, False)
    assert device.actual_angle == NumericValue(1, 1, 10, False)
    assert device.actions == list(Action)


def test_init_device_unknown():
    device = init_device(
        "id",
        "name",
        DeviceType.UNKNOWN,
    )
    assert isinstance(device, Device)
    assert device.identifier == "id"
    assert device.name == "name"
    assert device.device_type == DeviceType.UNKNOWN
    assert device.device_mode.mode == DeviceType.UNKNOWN


def test_init_device_no_type():
    device = init_device(
        "id",
        "name",
    )
    assert isinstance(device, Device)
    assert device.identifier == "id"
    assert device.name == "name"
    assert device.device_type == DeviceType.UNKNOWN
    assert device.device_mode.mode is None


def test_init_device_no_data():
    device = init_device(
        "id",
    )
    assert isinstance(device, Device)
    assert device.identifier == "id"
    assert device.name is None
    assert device.device_type == DeviceType.UNKNOWN
    assert device.device_mode.mode is None
