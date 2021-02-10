"""Tests for the Shutter Device class."""
import pytest

from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.shutter import Shutter
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType


class TestShutter:
    @pytest.fixture
    def device_mode(self):
        yield DeviceMode(DeviceType.ROLLERSHUTTER)

    def test_init(self, device_mode):
        value1 = NumericValue(10, 0, 10, False)
        value2 = NumericValue(1, 0, 10, False)
        shutter = Shutter(
            "id",
            "name",
            DeviceType.AWNING,
            device_mode,
            list(Action),
            value1,
            value2,
            value1,
            value2,
            value1,
            value2,
            value1,
        )
        assert shutter.identifier == "id"
        assert shutter.device_type == DeviceType.AWNING
        assert shutter.device_mode.mode == DeviceType.ROLLERSHUTTER
        assert shutter.target_position == value1
        assert shutter.target_angle == value2
        assert shutter.actual_angle == value1
        assert shutter.actual_position == value2
        assert shutter.drivetime_down == value1
        assert shutter.drivetime_up == value2
        assert shutter.rotationtime == value1

    def test_init_no_additional_values(self, device_mode):
        shutter = Shutter("id", "name", DeviceType.AWNING, device_mode, [])
        assert shutter.identifier == "id"
        assert shutter.device_type == DeviceType.AWNING
        assert shutter.device_mode.mode == DeviceType.ROLLERSHUTTER
        assert shutter.target_position is None
        assert shutter.target_angle is None
        assert shutter.actual_angle is None
        assert shutter.actual_position is None
        assert shutter.drivetime_down is None
        assert shutter.drivetime_up is None
        assert shutter.rotationtime is None
