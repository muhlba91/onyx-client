"""Tests for the Shutter Device class."""
import pytest

from onyx_client.data.boolean_value import BooleanValue
from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.shutter import Shutter
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType
from onyx_client.exception.update_exception import UpdateException


class TestShutter:
    @pytest.fixture
    def device_mode(self):
        yield DeviceMode(DeviceType.ROLLERSHUTTER)

    def test_init(self, device_mode):
        value1 = NumericValue(10, 0, 10, False)
        value2 = NumericValue(1, 0, 10, False)
        boolean1 = BooleanValue(False, True)
        boolean2 = BooleanValue(True, False)
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
            boolean1,
            boolean2,
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
        assert shutter.switch_button_direction == boolean1
        assert shutter.switch_drive_direction == boolean2

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
        assert shutter.switch_button_direction is None
        assert shutter.switch_drive_direction is None

    def test_update_with(self, device_mode):
        value1 = NumericValue(10, 0, 10, False)
        value2 = NumericValue(1, 0, 10, False)
        boolean1 = BooleanValue(False, True)
        boolean2 = BooleanValue(True, False)
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
            boolean1,
            boolean2,
        )
        update = Shutter(
            "id",
            "name1",
            DeviceType.AWNING,
            device_mode,
            list(Action),
            value2,
            value1,
            value2,
            value1,
            value2,
            value1,
            value2,
            boolean2,
            boolean1,
        )
        shutter.update_with(update)
        assert shutter.name == "name1"
        assert shutter.target_position == value2
        assert shutter.target_angle == value1
        assert shutter.actual_angle == value2
        assert shutter.actual_position == value1
        assert shutter.drivetime_down == value2
        assert shutter.drivetime_up == value1
        assert shutter.rotationtime == value2
        assert shutter.switch_button_direction == boolean2
        assert shutter.switch_drive_direction == boolean1

    def test_update_with_none(self, device_mode):
        value1 = NumericValue(10, 0, 10, False)
        value2 = NumericValue(1, 0, 10, False)
        boolean1 = BooleanValue(False, True)
        boolean2 = BooleanValue(True, False)
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
            boolean1,
            boolean2,
        )
        update = Shutter(
            "id",
            None,
            None,
            None,
            None,
        )
        shutter.update_with(update)
        assert shutter.name == "name"
        assert shutter.target_position == value1
        assert shutter.target_angle == value2
        assert shutter.actual_angle == value1
        assert shutter.actual_position == value2
        assert shutter.drivetime_down == value1
        assert shutter.drivetime_up == value2
        assert shutter.rotationtime == value1
        assert shutter.switch_button_direction == boolean1
        assert shutter.switch_drive_direction == boolean2

    def test_update_with_exception(self, device_mode):
        value1 = NumericValue(10, 0, 10, False)
        value2 = NumericValue(1, 0, 10, False)
        boolean1 = BooleanValue(False, True)
        boolean2 = BooleanValue(True, False)
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
            boolean1,
            boolean2,
        )
        update = Shutter(
            "other",
            None,
            None,
            None,
            None,
        )
        with pytest.raises(UpdateException):
            shutter.update_with(update)
