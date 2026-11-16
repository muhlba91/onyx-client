"""Onyx Client mapper utils."""

from ..data.active_command import ActiveCommand
from ..data.device_mode import DeviceMode
from ..data.enum_value import EnumValue
from ..data.numeric_value import NumericValue
from ..device.click import Click
from ..device.device import Device
from ..device.input import Input
from ..device.light import Light
from ..device.shutter import Shutter
from ..device.switch import Switch
from ..device.tag_sun import TagSun
from ..device.tag_temperature import TagTemperature
from ..device.weather import Weather
from ..enum.action import Action
from ..enum.device_type import DeviceType
from ..group.group import Group


def init_device(identifier: str, data: dict) -> Device:
    """Initialize the device from its complete API data.

    The device type is taken from the API's type only. Missing properties are None.

    identifier: the device identifier
    data: the device data as returned by the API"""
    raw_type = data.get("type")
    device_type = DeviceType.convert(raw_type)
    properties = data.get("properties") or {}

    def numeric(key: str) -> NumericValue | None:
        return NumericValue.create(properties.get(key))

    def enum(key: str) -> EnumValue | None:
        return EnumValue.create(properties.get(key))

    args = (
        identifier,
        data.get("name"),
        device_type,
        _device_mode(device_type, properties.get("device_type")),
        [Action.convert(action) for action in data.get("actions") or []],
    )
    kwargs = {
        "raw_type": raw_type,
        "tint": data.get("tint"),
        "active_command": ActiveCommand.create(data.get("active_command")),
    }

    if device_type.is_shutter():
        return Shutter(
            *args,
            target_position=numeric("target_position"),
            target_angle=numeric("target_angle"),
            actual_angle=numeric("actual_angle"),
            actual_position=numeric("actual_position"),
            system_state=enum("system_state"),
            temperature=numeric("temperature"),
            humidity=numeric("humidity"),
            **kwargs,
        )
    if device_type.is_light():
        return Light(
            *args,
            target_brightness=numeric("target_brightness"),
            actual_brightness=numeric("actual_brightness"),
            dim_duration=numeric("dim_duration"),
            target_hue=numeric("target_hue"),
            actual_hue=numeric("actual_hue"),
            target_saturation=numeric("target_saturation"),
            actual_saturation=numeric("actual_saturation"),
            target_color_temperature=numeric("target_color_temperature"),
            actual_color_temperature=numeric("actual_color_temperature"),
            color_mode=enum("color_mode"),
            **kwargs,
        )
    if device_type == DeviceType.WEATHER:
        return Weather(
            *args,
            wind_peak=numeric("wind_peak"),
            sun_brightness_peak=numeric("sun_brightness_peak"),
            sun_brightness_sink=numeric("sun_brightness_sink"),
            air_pressure=numeric("air_pressure"),
            humidity=numeric("humidity"),
            temperature=numeric("temperature"),
            wind_speed=numeric("wind_speed"),
            sun_brightness=numeric("sun_brightness"),
            **kwargs,
        )
    if device_type == DeviceType.TAG_SUN:
        return TagSun(
            *args,
            sun_brightness=numeric("sun_brightness"),
            sun_brightness_peak=numeric("sun_brightness_peak"),
            sun_brightness_sink=numeric("sun_brightness_sink"),
            **kwargs,
        )
    if device_type == DeviceType.TAG_TEMPERATURE:
        return TagTemperature(
            *args,
            temperature=numeric("temperature"),
            humidity=numeric("humidity"),
            **kwargs,
        )
    if device_type.is_input():
        return Input(
            *args,
            input_type=enum("input_type"),
            input_active=enum("input_active"),
            **kwargs,
        )
    if device_type == DeviceType.CLICK:
        return Click(*args, offline=data.get("offline", True), **kwargs)
    if device_type == DeviceType.SWITCH:
        return Switch(*args, **kwargs)
    return Device(*args, **kwargs)


def init_group(identifier: str, data: dict) -> Group:
    """Initialize the group from its API data.

    identifier: the group identifier
    data: the group data as returned by the API"""
    return Group(identifier, data.get("name"), data.get("devices") or [])


def _device_mode(device_type: DeviceType, properties: dict | None) -> DeviceMode:
    """Get the device mode from the device_type property, if present.

    device_type: the device type
    properties: the properties of the device_type property"""
    if properties is None:
        return DeviceMode(device_type)
    return DeviceMode(
        DeviceType.convert(properties.get("value")),
        [DeviceType.convert(value) for value in properties.get("values") or []],
    )
