"""Tests for the Light Device class."""

from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.enum_value import EnumValue
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.light import Light
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType


class TestLight:
    def test_init(self):
        brightness = NumericValue(100, 0, 65535, False)
        duration = NumericValue(5000, 0, 3600000, False)
        hue = NumericValue(120, 0, 359, False)
        saturation = NumericValue(50, 0, 100, False)
        temperature = NumericValue(4000, 2700, 10500, False)
        mode = EnumValue("hsv", ["hsv", "temperature"], True)
        light = Light(
            "id",
            "name",
            DeviceType.RGBW_LIGHT,
            DeviceMode(DeviceType.RGBW_LIGHT),
            list(Action),
            brightness,
            brightness,
            duration,
            hue,
            hue,
            saturation,
            saturation,
            temperature,
            temperature,
            mode,
        )
        assert light.identifier == "id"
        assert light.name == "name"
        assert light.device_type == DeviceType.RGBW_LIGHT
        assert light.device_mode.mode == DeviceType.RGBW_LIGHT
        assert light.actions == list(Action)
        assert light.target_brightness == brightness
        assert light.actual_brightness == brightness
        assert light.dim_duration == duration
        assert light.target_hue == hue
        assert light.actual_hue == hue
        assert light.target_saturation == saturation
        assert light.actual_saturation == saturation
        assert light.target_color_temperature == temperature
        assert light.actual_color_temperature == temperature
        assert light.color_mode == mode

    def test_init_defaults(self):
        light = Light("id", "name", DeviceType.BASIC_LIGHT, None, [])
        assert light.target_brightness is None
        assert light.target_hue is None
        assert light.color_mode is None

    def test_str(self):
        value = NumericValue(10, 0, 100, False)
        light = Light("id", "name", DeviceType.DIMMABLE_LIGHT, None, [], value, value)
        assert (
            str(light)
            == "Light(Device(id=id, name=name, type=DeviceType.DIMMABLE_LIGHT), actual_brightness=NumericValue(value=10, minimum=0, maximum=100, animation=None), target_brightness=NumericValue(value=10, minimum=0, maximum=100, animation=None), dim_duration=None, color_mode=None)"
        )

    def test_init_common_attributes(self):
        light = Light("id", "name", DeviceType.BASIC_LIGHT, None, [], tint="#000000")
        assert light.tint == "#000000"
