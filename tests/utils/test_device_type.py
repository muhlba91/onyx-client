"""Tests for device type utils."""
from onyx_client.enum.device_type import DeviceType
from onyx_client.utils.device_type import is_shutter, is_light, is_weather, is_click


def test_is_shutter():
    assert is_shutter(DeviceType.ROLLERSHUTTER, {})
    assert not is_shutter(DeviceType.WEATHER, {})
    assert not is_shutter(None, {})
    assert not is_shutter(None, None)
    assert is_shutter(None, {"target_position": 10})
    assert not is_shutter(None, {"sun_brightness_sink": 10})


def test_is_light():
    assert is_light(DeviceType.BASIC_LIGHT, {})
    assert not is_light(DeviceType.WEATHER, {})
    assert not is_light(None, {})
    assert not is_light(None, None)
    assert is_light(None, {"target_brightness": 10})
    assert not is_light(None, {"target_position": 10})


def test_is_weather():
    assert is_weather(DeviceType.WEATHER, {})
    assert not is_weather(DeviceType.BASIC_LIGHT, {})
    assert not is_weather(None, {})
    assert not is_weather(None, None)
    assert is_weather(None, {"sun_brightness_sink": 10})
    assert not is_weather(None, {"target_position": 10})


def test_is_click():
    assert is_click(DeviceType.CLICK, {})
    assert not is_click(DeviceType.BASIC_LIGHT, {})
    assert not is_click(None, {})
    assert not is_click(None, None)
    assert is_click(None, {"offline": 10})
    assert not is_click(None, {"target_position": 10})
