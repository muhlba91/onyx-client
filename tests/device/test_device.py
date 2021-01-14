"""Tests for the Base Device class."""
import pytest

from onyx_client.data.device_mode import DeviceMode
from onyx_client.device.device import Device
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType


class TestDevice:
    @pytest.fixture
    def device_mode(self):
        yield DeviceMode(DeviceType.ROLLERSHUTTER)

    def test_init(self, device_mode):
        device = Device("id", "name", DeviceType.AWNING, device_mode, list(Action))
        assert device.identifier == "id"
        assert device.device_type == DeviceType.AWNING
        assert device.device_mode.mode == DeviceType.ROLLERSHUTTER

    def test_eq(self, device_mode):
        assert Device(
            "id", "name", DeviceType.AWNING, device_mode, list(Action)
        ) == Device("id", "name1", DeviceType.AWNING, device_mode, list(Action))

    def test_not_eq(self, device_mode):
        assert Device("id", "name", DeviceType.AWNING, device_mode, list(Action)) != 10
