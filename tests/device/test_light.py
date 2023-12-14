"""Tests for the Light Device class."""
import pytest
import pytest_asyncio

from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.light import Light
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType
from onyx_client.exception.update_exception import UpdateException


class TestLight:
    @pytest_asyncio.fixture
    def device_mode(self):
        yield DeviceMode(DeviceType.BASIC_LIGHT)

    def test_init(self, device_mode):
        value1 = NumericValue(1, 0, 10, False)
        value2 = NumericValue(2, 0, 10, False)
        value3 = NumericValue(3, 0, 10, False)
        light = Light(
            "id",
            "name",
            DeviceType.BASIC_LIGHT,
            device_mode,
            list(Action),
            value1,
            value2,
            value3,
        )
        assert light.identifier == "id"
        assert light.device_type == DeviceType.BASIC_LIGHT
        assert light.device_mode.mode == DeviceType.BASIC_LIGHT
        assert light.target_brightness == value1
        assert light.actual_brightness == value2
        assert light.dim_duration == value3

    def test_str(self):
        value1 = NumericValue(1, 0, 10, False)
        value2 = NumericValue(2, 0, 10, False)
        value3 = NumericValue(3, 0, 10, False)
        light = Light(
            "id",
            "name",
            DeviceType.BASIC_LIGHT,
            None,
            list(Action),
            value1,
            value2,
            value3,
        )
        assert (
            str(light)
            == "Light(Device(id=id, name=name, type=DeviceType.BASIC_LIGHT), actual_brightness=NumericValue(value=2, minimum=0, maximum=10, animation=None), target_brightness=NumericValue(value=1, minimum=0, maximum=10, animation=None), dim_duration=NumericValue(value=3, minimum=0, maximum=10, animation=None))"
        )

    def test_init_no_additional_values(self, device_mode):
        light = Light(
            "id",
            "name",
            DeviceType.BASIC_LIGHT,
            device_mode,
            list(Action),
        )
        assert light.identifier == "id"
        assert light.device_type == DeviceType.BASIC_LIGHT
        assert light.device_mode.mode == DeviceType.BASIC_LIGHT
        assert light.target_brightness is None
        assert light.actual_brightness is None
        assert light.dim_duration is None

    def test_update_with(self, device_mode):
        value1 = NumericValue(1, 0, 10, False)
        value2 = NumericValue(2, 0, 10, False)
        value3 = NumericValue(3, 0, 10, False)
        light = Light(
            "id",
            "name",
            DeviceType.BASIC_LIGHT,
            device_mode,
            list(Action),
            value1,
            value2,
            value3,
        )
        update = Light(
            "id",
            "name1",
            DeviceType.BASIC_LIGHT,
            device_mode,
            list(Action),
            value3,
            value2,
            value1,
        )
        light.update_with(update)
        assert light.name == "name1"
        assert light.target_brightness == value3
        assert light.actual_brightness == value2
        assert light.dim_duration == value1

    def test_update_with_none(self, device_mode):
        value1 = NumericValue(1, 0, 10, False)
        value2 = NumericValue(2, 0, 10, False)
        value3 = NumericValue(3, 0, 10, False)
        light = Light(
            "id",
            "name",
            DeviceType.BASIC_LIGHT,
            device_mode,
            list(Action),
            value1,
            value2,
            value3,
        )
        update = Light(
            "id",
            None,
            None,
            None,
            None,
        )
        light.update_with(update)
        assert light.name == "name"
        assert light.target_brightness == value1
        assert light.actual_brightness == value2
        assert light.dim_duration == value3

    def test_update_with_exception(self, device_mode):
        value1 = NumericValue(1, 0, 10, False)
        value2 = NumericValue(2, 0, 10, False)
        value3 = NumericValue(3, 0, 10, False)
        light = Light(
            "id",
            "name",
            DeviceType.BASIC_LIGHT,
            device_mode,
            list(Action),
            value1,
            value2,
            value3,
        )
        update = Light(
            "other",
            None,
            None,
            None,
            None,
        )
        with pytest.raises(UpdateException):
            light.update_with(update)

    def test_update_with_partials(self, device_mode):
        value1 = NumericValue(1, 0, 10, False)
        value2 = NumericValue(2, 0, 10, False)
        value3 = NumericValue(3, 0, 10, False)
        value4 = NumericValue(None, 10, None, False)
        value5 = NumericValue(20, None, None, False)
        value6 = NumericValue(None, None, 100, False)
        light = Light(
            "id",
            "name",
            DeviceType.BASIC_LIGHT,
            device_mode,
            list(Action),
            value1,
            value2,
            value3,
        )
        update = Light(
            "id",
            "name1",
            DeviceType.BASIC_LIGHT,
            device_mode,
            list(Action),
            value4,
            value5,
            value6,
        )
        light.update_with(update)
        assert light.name == "name1"
        assert light.target_brightness == NumericValue(1, 10, 10, False)
        assert light.actual_brightness == NumericValue(20, 0, 10, False)
        assert light.dim_duration == NumericValue(3, 0, 100, False)

        value1 = NumericValue(1, 0, 10, False)
        value2 = NumericValue(2, 0, 10, False)
        value3 = NumericValue(3, 0, 10, False)
        light = Light(
            "id",
            "name",
            DeviceType.BASIC_LIGHT,
            device_mode,
            list(Action),
            None,
            value2,
            value3,
        )
        update = Light(
            "id",
            "name1",
            DeviceType.BASIC_LIGHT,
            device_mode,
            list(Action),
            value1,
            None,
            None,
        )
        light.update_with(update)
        assert light.name == "name1"
        assert light.target_brightness == value1
        assert light.actual_brightness == value2
        assert light.dim_duration == value3
