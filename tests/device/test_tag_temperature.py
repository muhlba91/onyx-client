"""Tests for the TagTemperature Device class."""

from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.tag_temperature import TagTemperature
from onyx_client.enum.device_type import DeviceType


class TestTagTemperature:
    def test_init(self):
        temperature = NumericValue(215, -400, 1500, True)
        humidity = NumericValue(40, 0, 100, True)
        tag = TagTemperature(
            "id",
            "name",
            DeviceType.TAG_TEMPERATURE,
            DeviceMode(DeviceType.TAG_TEMPERATURE),
            [],
            temperature,
            humidity,
            tint="#FFFFFF",
        )
        assert tag.identifier == "id"
        assert tag.device_type == DeviceType.TAG_TEMPERATURE
        assert tag.temperature == temperature
        assert tag.humidity == humidity
        assert tag.tint == "#FFFFFF"

    def test_str(self):
        assert (
            str(TagTemperature("id", "name", DeviceType.TAG_TEMPERATURE, None, []))
            == "TagTemperature(Device(id=id, name=name, type=DeviceType.TAG_TEMPERATURE), temperature=None, humidity=None)"
        )

    def test_init_common_attributes(self):
        device = TagTemperature(
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
