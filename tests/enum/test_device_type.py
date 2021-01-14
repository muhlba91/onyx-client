"""Tests for the Action enum."""
import pytest

from onyx_client.enum.device_type import DeviceType


class TestDeviceType:
    def test_convert(self):
        assert DeviceType.convert(DeviceType.AWNING.name.lower()) == DeviceType.AWNING

    def test_convert_invalid(self):
        assert not DeviceType.convert("foo")

    @pytest.mark.parametrize("device_type", list(DeviceType))
    def test_string(self, device_type: DeviceType):
        assert device_type.string() == device_type.name.lower()

    def test_is_shutter(self):
        assert DeviceType.AWNING.is_shutter()
        assert DeviceType.ROLLERSHUTTER.is_shutter()
        assert DeviceType.RAFFSTORE_90.is_shutter()
        assert DeviceType.RAFFSTORE_180.is_shutter()
