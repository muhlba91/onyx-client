"""Tests for the DeviceMode data class."""
from onyx_client.data.device_mode import DeviceMode
from onyx_client.enum.device_type import DeviceType


class TestDeviceMode:
    def test_init(self):
        mode = DeviceMode(DeviceType.ROLLERSHUTTER)
        assert mode.mode == DeviceType.ROLLERSHUTTER
        assert mode.values is None

    def test_init_with_values(self):
        mode = DeviceMode(DeviceType.ROLLERSHUTTER, [DeviceType.AWNING])
        assert mode.mode == DeviceType.ROLLERSHUTTER
        assert DeviceType.AWNING in mode.values
