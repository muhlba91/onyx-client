"""Tests for the DeviceType enum."""

import pytest

from onyx_client.enum.device_type import DeviceType


class TestDeviceType:
    def test_convert(self):
        assert DeviceType.convert(DeviceType.AWNING.name.lower()) == DeviceType.AWNING

    def test_convert_invalid(self):
        assert DeviceType.convert("foo") == DeviceType.UNKNOWN

    @pytest.mark.parametrize("device_type", list(DeviceType))
    def test_string(self, device_type: DeviceType):
        assert device_type.string() == device_type.name.lower()

    def test_is_shutter(self):
        assert DeviceType.AWNING.is_shutter()
        assert DeviceType.ROLLERSHUTTER.is_shutter()
        assert DeviceType.RAFFSTORE_90.is_shutter()
        assert DeviceType.RAFFSTORE_180.is_shutter()
        assert DeviceType.VENEER.is_shutter()
        assert DeviceType.PERGOLA_AWNING_ROOF.is_shutter()
        assert DeviceType.PERGOLA_SIDE.is_shutter()
        assert DeviceType.PERGOLA_SLAT_ROOF.is_shutter()
        assert DeviceType.SCREEN.is_shutter()

    def test_is_light(self):
        assert DeviceType.BASIC_LIGHT.is_light()
        assert DeviceType.DIMMABLE_LIGHT.is_light()
        assert DeviceType.RGBW_LIGHT.is_light()

    def test_is_input(self):
        assert DeviceType.INPUT.is_input()
        assert not DeviceType.INPUT.is_shutter()
        assert not DeviceType.WEATHER.is_input()

    def test_is_tag(self):
        assert DeviceType.TAG_SUN.is_tag()
        assert DeviceType.TAG_TEMPERATURE.is_tag()
        assert not DeviceType.WEATHER.is_tag()
        assert not DeviceType.TAG_SUN.is_shutter()
        assert not DeviceType.TAG_SUN.is_light()

    def test_convert_tags(self):
        assert DeviceType.convert("tag_sun") == DeviceType.TAG_SUN
        assert DeviceType.convert("tag_temperature") == DeviceType.TAG_TEMPERATURE

    def test_convert_v6_types(self):
        assert DeviceType.convert("rgbw_light") == DeviceType.RGBW_LIGHT
        assert DeviceType.convert("screen") == DeviceType.SCREEN
        assert DeviceType.convert("input") == DeviceType.INPUT

    def test_convert_none(self):
        assert DeviceType.convert(None) == DeviceType.UNKNOWN

    def test_is_shutter_false_for_non_shutter(self):
        assert not DeviceType.BASIC_LIGHT.is_shutter()
        assert not DeviceType.DIMMABLE_LIGHT.is_shutter()
