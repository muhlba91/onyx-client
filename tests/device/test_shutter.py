"""Tests for the Shutter Device class."""

import pytest
import pytest_asyncio

from onyx_client.data.animation_keyframe import AnimationKeyframe
from onyx_client.data.animation_value import AnimationValue
from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.shutter import Shutter
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType
from onyx_client.exception.update_exception import UpdateException


class TestShutter:
    @pytest_asyncio.fixture
    def device_mode(self):
        yield DeviceMode(DeviceType.ROLLERSHUTTER)

    def test_init(self, device_mode):
        value1 = NumericValue(10, 0, 10, False)
        value2 = NumericValue(
            1,
            0,
            10,
            False,
            AnimationValue(10.4, 10, [AnimationKeyframe("linear", 0, 100.2, 10)]),
        )
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
        )
        assert shutter.identifier == "id"
        assert shutter.device_type == DeviceType.AWNING
        assert shutter.device_mode.mode == DeviceType.ROLLERSHUTTER
        assert shutter.target_position == value1
        assert shutter.target_angle == value2
        assert shutter.actual_angle == value1
        assert shutter.actual_position == value2

    def test_str(self):
        value1 = NumericValue(10, 0, 10, False)
        value2 = NumericValue(
            1,
            0,
            10,
            False,
            AnimationValue(10.4, 10, [AnimationKeyframe("linear", 0, 100.2, 10)]),
        )
        shutter = Shutter(
            "id",
            "name",
            DeviceType.AWNING,
            None,
            list(Action),
            value1,
            value2,
            value1,
            value2,
        )
        assert (
            str(shutter)
            == "Shutter(Device(id=id, name=name, type=DeviceType.AWNING), actual_position=NumericValue(value=1, minimum=0, maximum=10, animation=AnimationValue(start=10.4, current_value=10, #keyframes=1)), actual_angle=NumericValue(value=10, minimum=0, maximum=10, animation=None), target_position=NumericValue(value=10, minimum=0, maximum=10, animation=None), target_angle=NumericValue(value=1, minimum=0, maximum=10, animation=AnimationValue(start=10.4, current_value=10, #keyframes=1)))"
        )

    def test_init_no_additional_values(self, device_mode):
        shutter = Shutter("id", "name", DeviceType.AWNING, device_mode, [])
        assert shutter.identifier == "id"
        assert shutter.device_type == DeviceType.AWNING
        assert shutter.device_mode.mode == DeviceType.ROLLERSHUTTER
        assert shutter.target_position is None
        assert shutter.target_angle is None
        assert shutter.actual_angle is None
        assert shutter.actual_position is None

    def test_update_with(self, device_mode):
        value1 = NumericValue(10, 0, 10, False)
        value2 = NumericValue(
            1,
            0,
            10,
            False,
            AnimationValue(10.4, 10, [AnimationKeyframe("linear", 0, 100.2, 10)]),
        )
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
        )
        shutter.update_with(update)
        assert shutter.name == "name1"
        assert shutter.target_position == value2
        assert shutter.target_angle == value1
        assert shutter.actual_angle == value2
        assert shutter.actual_position == value1

    def test_update_with_none(self, device_mode):
        value1 = NumericValue(10, 0, 10, False)
        value2 = NumericValue(
            1,
            0,
            10,
            False,
            AnimationValue(10.4, 10, [AnimationKeyframe("linear", 0, 100.2, 10)]),
        )
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

    def test_update_with_exception(self, device_mode):
        value1 = NumericValue(10, 0, 10, False)
        value2 = NumericValue(
            1,
            0,
            10,
            False,
            AnimationValue(10.4, 10, [AnimationKeyframe("linear", 0, 100.2, 10)]),
        )
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

    def test_update_with_partials(self, device_mode):
        value1 = NumericValue(1, 0, 10, False)
        value2 = NumericValue(2, 0, 10, False)
        value3 = NumericValue(3, 0, 10, False)
        value4 = NumericValue(4, 0, 10, False)
        value5 = NumericValue(10, None, None, False)
        value6 = NumericValue(None, 10, None, False)
        value7 = NumericValue(None, None, 100, False)
        value8 = NumericValue(None, None, None, False)
        shutter = Shutter(
            "id",
            "name",
            DeviceType.AWNING,
            device_mode,
            list(Action),
            value1,
            value2,
            value3,
            value4,
        )
        update = Shutter(
            "id",
            "name1",
            DeviceType.AWNING,
            device_mode,
            list(Action),
            value5,
            value6,
            value7,
            value8,
        )
        shutter.update_with(update)
        assert shutter.name == "name1"
        assert shutter.target_position == NumericValue(10, 0, 10, False)
        assert shutter.target_angle == NumericValue(2, 10, 10, False)
        assert shutter.actual_angle == NumericValue(3, 0, 100, False)
        assert shutter.actual_position == NumericValue(4, 0, 10, False)

        value1 = NumericValue(1, 0, 10, False)
        value2 = NumericValue(2, 0, 10, False)
        value3 = NumericValue(3, 0, 10, False)
        value4 = NumericValue(4, 0, 10, False)
        shutter = Shutter(
            "id",
            "name",
            DeviceType.AWNING,
            device_mode,
            list(Action),
            None,
            None,
            value3,
            value4,
        )
        update = Shutter(
            "id",
            "name1",
            DeviceType.AWNING,
            device_mode,
            list(Action),
            value1,
            value2,
            None,
            None,
        )
        shutter.update_with(update)
        assert shutter.name == "name1"
        assert shutter.target_position == value1
        assert shutter.target_angle == value2
        assert shutter.actual_angle == value3
        assert shutter.actual_position == value4
