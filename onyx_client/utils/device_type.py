"""Onyx Client device type utils."""

from ..device.click import Click
from ..device.light import Light
from ..device.shutter import Shutter
from ..device.switch import Switch
from ..device.tag_sun import TagSun
from ..device.weather import Weather
from ..enum.device_type import DeviceType


def is_shutter(device_type: DeviceType, properties: dict) -> bool:
    """Check if the provided device type is a shutter.

    device_type: the device type to check
    properties: the property map to check if no explicit type is specified"""
    if device_type is not None:
        return device_type.is_shutter()
    return _in_keys(properties, Shutter.keys())


def is_light(device_type: DeviceType, properties: dict) -> bool:
    """Check if the provided device type is a light.

    device_type: the device type to check
    properties: the property map to check if no explicit type is specified"""
    if device_type is not None:
        return device_type.is_light()
    return _in_keys(properties, Light.keys())


def is_weather(device_type: DeviceType, properties: dict) -> bool:
    """Check if the provided device type is a weather station.

    device_type: the device type to check
    properties: the property map to check if no explicit type is specified"""
    if device_type is not None:
        return device_type == DeviceType.WEATHER
    return _in_keys(properties, Weather.keys())


def is_tag_sun(device_type: DeviceType, properties: dict) -> bool:
    """Check if the provided device type is a sun tag.

    Without an explicit type, only a patch consisting solely of sun tag keys and
    containing the current brightness is a sun tag: the weather station reports
    the brightness as well, but also other values like the wind speed.

    device_type: the device type to check
    properties: the property map to check if no explicit type is specified"""
    if device_type is not None:
        return device_type == DeviceType.TAG_SUN
    tag_keys = TagSun.keys()
    return (
        properties is not None
        and "sun_brightness" in properties
        and all(key in tag_keys for key in properties)
    )


def is_tag_temperature(device_type: DeviceType, properties: dict) -> bool:
    """Check if the provided device type is a temperature tag.

    Without an explicit type, temperature and humidity patches cannot be told
    apart from weather station patches. They are mapped to a weather station,
    which carries both values, so updating an existing tag still works.

    device_type: the device type to check
    properties: the property map (unused, kept for a uniform signature)"""
    return device_type == DeviceType.TAG_TEMPERATURE


def is_click(device_type: DeviceType, data: dict) -> bool:
    """Check if the provided device type is a click device.

    device_type: the device type to check
    properties: the property map to check if no explicit type is specified"""
    if device_type is not None:
        return device_type == DeviceType.CLICK
    return _in_keys(data, Click.keys())


def is_switch(device_type: DeviceType, data: dict) -> bool:
    """Check if the provided device type is a switch.

    device_type: the device type to check
    properties: the property map to check if no explicit type is specified"""
    if device_type is not None:
        return device_type == DeviceType.SWITCH
    return _in_keys(data, Switch.keys())  # pragma: no mutate


def _in_keys(data: dict | None, keys: list) -> bool:
    """Check if any key in data is listed in the keys list.

    data: the data map to check
    keys: the keys to check for"""
    if data is not None:
        for key in data:
            if key in keys:
                return True
    return False
