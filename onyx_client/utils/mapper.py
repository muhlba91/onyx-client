"""Onyx Client mapper utils."""
from onyx_client.data.boolean_value import BooleanValue
from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.click import Click
from onyx_client.device.device import Device
from onyx_client.device.light import Light
from onyx_client.device.shutter import Shutter
from onyx_client.device.switch import Switch
from onyx_client.device.weather import Weather
from onyx_client.enum.device_type import DeviceType
from onyx_client.utils.device_type import (
    is_click,
    is_light,
    is_weather,
    is_shutter,
    is_switch,
)


def numeric_value(key: str, properties: dict = None):
    return (
        NumericValue.create(properties.get(key, None))
        if properties is not None
        else None
    )


def boolean_value(key: str, properties: dict = None):
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
    """Initialize the device correctly."""
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
