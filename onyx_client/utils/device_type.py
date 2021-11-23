"""Onyx Client device type utils."""
from onyx_client.device.click import Click
from onyx_client.device.light import Light
from onyx_client.device.shutter import Shutter
from onyx_client.device.weather import Weather
from onyx_client.enum.device_type import DeviceType


def is_shutter(device_type: DeviceType, properties: dict) -> bool:
    if device_type is not None:
        return device_type.is_shutter()
    if properties is not None:
        for key in properties.keys():
            if key in Shutter.keys():
                return True
    return False


def is_light(device_type: DeviceType, properties: dict) -> bool:
    if device_type is not None:
        return device_type == DeviceType.BASIC_LIGHT
    if properties is not None:
        for key in properties.keys():
            if key in Light.keys():
                return True
    return False


def is_weather(device_type: DeviceType, properties: dict) -> bool:
    if device_type is not None:
        return device_type == DeviceType.WEATHER
    if properties is not None:
        for key in properties.keys():
            if key in Weather.keys():
                return True
    return False


def is_click(device_type: DeviceType, data: dict) -> bool:
    if device_type is not None:
        return device_type == DeviceType.CLICK
    if data is not None:
        for key in data.keys():
            if key in Click.keys():
                return True
    return False
