"""Onyx Client device type utils."""
from typing import Optional

from onyx_client.device.click import Click
from onyx_client.device.light import Light
from onyx_client.device.shutter import Shutter
from onyx_client.device.switch import Switch
from onyx_client.device.weather import Weather
from onyx_client.enum.device_type import DeviceType


def is_shutter(device_type: DeviceType, properties: dict) -> bool:
    """Checks if the provided device is a shutter."""
    if device_type is not None:
        return device_type.is_shutter()
    return _in_keys(properties, Shutter.keys())


def is_light(device_type: DeviceType, properties: dict) -> bool:
    """Checks if the provided device is a light."""
    if device_type is not None:
        return device_type == DeviceType.BASIC_LIGHT
    return _in_keys(properties, Light.keys())


def is_weather(device_type: DeviceType, properties: dict) -> bool:
    """Checks if the provided device is a weather station."""
    if device_type is not None:
        return device_type == DeviceType.WEATHER
    return _in_keys(properties, Weather.keys())


def is_click(device_type: DeviceType, data: dict) -> bool:
    """Checks if the provided device is a click device."""
    if device_type is not None:
        return device_type == DeviceType.CLICK
    return _in_keys(data, Click.keys())


def is_switch(device_type: DeviceType, data: dict) -> bool:
    """Checks if the provided device is a switch."""
    if device_type is not None:
        return device_type == DeviceType.SWITCH
    return _in_keys(data, Switch.keys())


def _in_keys(data: Optional[dict], keys: list) -> bool:
    """Checks if any key in data is listed in the keys list."""
    if data is not None:
        for key in data.keys():
            if key in keys:
                return True
    return False
