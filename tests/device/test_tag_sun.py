"""Tests for the TagSun Device class."""

from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.tag_sun import TagSun
from onyx_client.enum.device_type import DeviceType


class TestTagSun:
    def test_init(self):
        values = [NumericValue(index, 0, 150000, True) for index in range(3)]
        tag = TagSun(
            "id",
            "name",
            DeviceType.TAG_SUN,
            DeviceMode(DeviceType.TAG_SUN),
            [],
            *values,
            tint="#FFFFFF",
        )
        assert tag.identifier == "id"
        assert tag.device_type == DeviceType.TAG_SUN
        assert tag.sun_brightness == values[0]
        assert tag.sun_brightness_peak == values[1]
        assert tag.sun_brightness_sink == values[2]
        assert tag.tint == "#FFFFFF"

    def test_str(self):
        assert (
            str(TagSun("id", "name", DeviceType.TAG_SUN, None, []))
            == "TagSun(Device(id=id, name=name, type=DeviceType.TAG_SUN), sun_brightness=None, sun_brightness_peak=None, sun_brightness_sink=None)"
        )

    def test_init_common_attributes(self):
        device = TagSun(
            "id",
            "name",
            DeviceType.UNKNOWN,
            DeviceMode(DeviceType.UNKNOWN),
            [None],
            tint="#000000",
        )
        assert device.device_mode.mode == DeviceType.UNKNOWN
        assert device.actions == [None]
        assert device.tint == "#000000"
