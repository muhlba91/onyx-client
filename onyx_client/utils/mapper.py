"""Onyx Client mapper utils."""

from ..data.boolean_value import BooleanValue
from ..data.device_mode import DeviceMode
from ..data.numeric_value import NumericValue
from ..device.click import Click
from ..device.device import Device
from ..device.light import Light
from ..device.shutter import Shutter
from ..device.switch import Switch
from ..device.weather import Weather
from ..enum.device_type import DeviceType
from ..utils.device_type import (
    is_click,
    is_light,
    is_weather,
    is_shutter,
    is_switch,
)


def numeric_value(key: str, properties: dict = None):
    """Create a new numeric value.

    key: the key value
    properties: the device properties"""
    return (
        NumericValue.create(properties.get(key, None))
        if properties is not None
        else None
    )


def boolean_value(key: str, properties: dict = None):
    """Create a new boolean value.

    key: the key value
    properties: the device properties"""
    return (
        BooleanValue.create(properties.get(key, None))
        if properties is not None
        else None
    )


def init_device(
    identifier: str,
    name: str = None,
    device_type: DeviceType = None,
    properties: dict = None,
    actions: list = None,
    data: dict = None,
) -> Device:
    """Initialize the device correctly.

    identifier: the device identifier
    name: the device name
    device_type: the device type
    properties: the properties of the device to set
    actions: a list of actions the device supports
    data: the data map of the device"""
    device_mode_value = (
        DeviceType.convert(properties.get("device_type", dict()).get("type", None))
        if properties is not None
        else device_type
    )
    device_mode_values = (
        [
            DeviceType.convert(value)
            for value in properties.get("device_type", dict()).get("values", list())
        ]
        if properties is not None
        else None
    )
    device_mode = DeviceMode(device_mode_value, device_mode_values)
    if is_shutter(device_type, properties):
        return Shutter(
            identifier,
            name,
            device_type,
            device_mode,
            actions,
            numeric_value("target_position", properties),
            numeric_value("target_angle", properties),
            numeric_value("actual_angle", properties),
            numeric_value("actual_position", properties),
        )
    elif is_weather(device_type, properties):
        return Weather(
            identifier,
            name,
            device_type,
            device_mode,
            actions,
            numeric_value("wind_peak", properties),
            numeric_value("sun_brightness_peak", properties),
            numeric_value("sun_brightness_sink", properties),
            numeric_value("air_pressure", properties),
            numeric_value("humidity", properties),
            numeric_value("temperature", properties),
        )
    elif is_light(device_type, properties):
        return Light(
            identifier,
            name,
            device_type,
            device_mode,
            actions,
            numeric_value("target_brightness", properties),
            numeric_value("actual_brightness", properties),
            numeric_value("dim_duration", properties),
        )
    elif is_click(device_type, data):
        offline = data.get("offline", True) if data is not None else True
        return Click(identifier, name, device_type, offline)
    elif is_switch(device_type, data):
        return Switch(identifier, name, device_type)
    else:
        return Device(identifier, name, DeviceType.UNKNOWN, device_mode, actions)
