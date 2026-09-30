"""Tests for the TagSun Device class."""

import pytest
import pytest_asyncio

from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.device import Device
from onyx_client.device.tag_sun import TagSun
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType
from onyx_client.exception.update_exception import UpdateException


class TestTagSun:
    @pytest_asyncio.fixture
    def device_mode(self):
        yield DeviceMode(DeviceType.TAG_SUN)

    def values(self):
        return [NumericValue(i, 0, 10, False) for i in range(1, 3 + 1)]

    def test_init(self, device_mode):
        values = self.values()
        tag = TagSun(
            "id", "name", DeviceType.TAG_SUN, device_mode, list(Action), *values
        )
        assert tag.identifier == "id"
        assert tag.name == "name"
        assert tag.device_type == DeviceType.TAG_SUN
        assert tag.device_mode.mode == DeviceType.TAG_SUN
        assert tag.actions == list(Action)
        assert tag.sun_brightness == values[0]
        assert tag.sun_brightness_peak == values[1]
        assert tag.sun_brightness_sink == values[2]

    def test_str(self):
        tag = TagSun(
            "id", "name", DeviceType.TAG_SUN, None, list(Action), *self.values()
        )
        assert (
            str(tag)
            == "TagSun(Device(id=id, name=name, type=DeviceType.TAG_SUN), sun_brightness=NumericValue(value=1, minimum=0, maximum=10, animation=None), sun_brightness_peak=NumericValue(value=2, minimum=0, maximum=10, animation=None), sun_brightness_sink=NumericValue(value=3, minimum=0, maximum=10, animation=None))"
        )

    def test_init_no_additional_values(self, device_mode):
        tag = TagSun("id", "name", DeviceType.TAG_SUN, device_mode, list(Action))
        assert tag.sun_brightness is None
        assert tag.sun_brightness_peak is None
        assert tag.sun_brightness_sink is None

    def test_update_with(self, device_mode):
        values = self.values()
        tag = TagSun(
            "id", "name", DeviceType.TAG_SUN, device_mode, list(Action), *values
        )
        update = TagSun(
            "id",
            "name1",
            DeviceType.TAG_SUN,
            device_mode,
            list(Action),
            *reversed(values),
        )
        tag.update_with(update)
        assert tag.name == "name1"
        assert tag.sun_brightness == values[2]
        assert tag.sun_brightness_peak == values[1]
        assert tag.sun_brightness_sink == values[0]

    def test_update_with_no_data_update_data(self, device_mode):
        values = self.values()
        tag = TagSun("id", "name", DeviceType.TAG_SUN, device_mode, list(Action))
        update = TagSun(
            "id", "name1", DeviceType.TAG_SUN, device_mode, list(Action), *values
        )
        tag.update_with(update)
        assert tag.sun_brightness == values[0]
        assert tag.sun_brightness_peak == values[1]
        assert tag.sun_brightness_sink == values[2]

    def test_update_with_no_data_update_none(self, device_mode):
        tag = TagSun("id", "name", DeviceType.TAG_SUN, device_mode, list(Action))
        update = TagSun("id", "name1", DeviceType.TAG_SUN, device_mode, list(Action))
        tag.update_with(update)
        assert tag.name == "name1"
        assert tag.sun_brightness is None
        assert tag.sun_brightness_peak is None
        assert tag.sun_brightness_sink is None

    def test_update_with_none(self, device_mode):
        values = self.values()
        tag = TagSun(
            "id", "name", DeviceType.TAG_SUN, device_mode, list(Action), *values
        )
        update = TagSun("id", None, None, None, None)
        tag.update_with(update)
        assert tag.name == "name"
        assert tag.device_type == DeviceType.TAG_SUN
        assert tag.sun_brightness == values[0]
        assert tag.sun_brightness_peak == values[1]
        assert tag.sun_brightness_sink == values[2]

    def test_update_with_exception(self, device_mode):
        tag = TagSun(
            "id", "name", DeviceType.TAG_SUN, device_mode, list(Action), *self.values()
        )
        update = TagSun("other", None, None, None, None)
        with pytest.raises(UpdateException):
            tag.update_with(update)

    def test_update_with_partials(self, device_mode):
        tag = TagSun(
            "id", "name", DeviceType.TAG_SUN, device_mode, list(Action), *self.values()
        )
        partials = [NumericValue(40 + i, None, None, False) for i in range(3)]
        tag.update_with(TagSun("id", None, None, None, None, *partials))
        assert tag.sun_brightness == NumericValue(40, 0, 10, False)
        assert tag.sun_brightness_peak == NumericValue(41, 0, 10, False)
        assert tag.sun_brightness_sink == NumericValue(42, 0, 10, False)

    def test_update_with_base_device_patch(self, device_mode):
        """A patch without tag values (e.g. only a name change) keeps all values."""
        values = self.values()
        tag = TagSun(
            "id", "name", DeviceType.TAG_SUN, device_mode, list(Action), *values
        )
        tag.update_with(Device("id", "name1", None, None, None))
        assert tag.name == "name1"
        assert tag.sun_brightness == values[0]
        assert tag.sun_brightness_peak == values[1]
        assert tag.sun_brightness_sink == values[2]

    def test_keys(self):
        assert TagSun.keys() == [
            "sun_brightness",
            "sun_brightness_peak",
            "sun_brightness_sink",
        ]
