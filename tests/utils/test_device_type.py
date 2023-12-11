"""Tests for device type utils."""
from onyx_client.enum.device_type import DeviceType
from onyx_client.utils.device_type import (
    is_shutter,
    is_light,
    is_weather,
    is_click,
    is_switch,
    _in_keys,
)


def test_is_shutter():
    assert is_shutter(DeviceType.ROLLERSHUTTER, {})
    assert is_shutter(DeviceType.AWNING, {})
    assert is_shutter(DeviceType.RAFFSTORE_90, {})
    assert is_shutter(DeviceType.RAFFSTORE_180, {})
    assert is_shutter(DeviceType.VENEER, {})
    assert is_shutter(DeviceType.PERGOLA_AWNING_ROOF, {})
    assert is_shutter(DeviceType.PERGOLA_SIDE, {})
    assert is_shutter(DeviceType.PERGOLA_SLAT_ROOF, {})
    assert not is_shutter(DeviceType.WEATHER, {})
    assert not is_shutter(None, {})
    assert not is_shutter(None, None)
    assert is_shutter(None, {"target_position": 10})
    assert not is_shutter(None, {"sun_brightness_sink": 10})


def test_is_light():
    assert is_light(DeviceType.BASIC_LIGHT, {})
    assert is_light(DeviceType.DIMMABLE_LIGHT, {})
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


def test_is_switch():
    assert is_switch(DeviceType.SWITCH, {})
    assert not is_switch(DeviceType.BASIC_LIGHT, {})
    assert not is_switch(None, {})
    assert not is_switch(None, None)
    assert not is_switch(None, {"target_position": 10})


def test__in_keys():
    assert _in_keys({"key": "value"}, ["key"])
    assert not _in_keys({"key": "value"}, ["other"])
    assert not _in_keys({"key": "value"}, [])
    assert not _in_keys({}, ["key"])
    assert not _in_keys(None, ["key"])
    assert not _in_keys(None, [])
