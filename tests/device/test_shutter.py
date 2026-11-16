"""Tests for the Shutter Device class."""

from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.enum_value import EnumValue
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.shutter import Shutter
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType


class TestShutter:
    def test_init(self):
        position = NumericValue(10, 0, 100, False)
        angle = NumericValue(90, 0, 360, True)
        state = EnumValue("ok", ["ok", "collision"], True)
        temperature = NumericValue(215, -400, 850, True)
        humidity = NumericValue(40, 0, 100, True)
        shutter = Shutter(
            "id",
            "name",
            DeviceType.PERGOLA_SLAT_ROOF,
            DeviceMode(DeviceType.PERGOLA_SLAT_ROOF),
            list(Action),
            position,
            angle,
            angle,
            position,
            state,
            temperature,
            humidity,
            tint="#FFFFFF",
        )
        assert shutter.identifier == "id"
        assert shutter.name == "name"
        assert shutter.device_type == DeviceType.PERGOLA_SLAT_ROOF
        assert shutter.device_mode.mode == DeviceType.PERGOLA_SLAT_ROOF
        assert shutter.actions == list(Action)
        assert shutter.target_position == position
        assert shutter.target_angle == angle
        assert shutter.actual_angle == angle
        assert shutter.actual_position == position
        assert shutter.system_state == state
        assert shutter.temperature == temperature
        assert shutter.humidity == humidity
        assert shutter.tint == "#FFFFFF"

    def test_init_defaults(self):
        shutter = Shutter("id", "name", DeviceType.ROLLERSHUTTER, None, [])
        assert shutter.target_position is None
        assert shutter.system_state is None
        assert shutter.temperature is None
        assert shutter.humidity is None

    def test_str(self):
        value = NumericValue(10, 0, 100, False)
        shutter = Shutter(
            "id",
            "name",
            DeviceType.AWNING,
            None,
            [],
            value,
            value,
            value,
            value,
            EnumValue("ok", [], True),
        )
        assert (
            str(shutter)
            == "Shutter(Device(id=id, name=name, type=DeviceType.AWNING), actual_position=NumericValue(value=10, minimum=0, maximum=100, animation=None), actual_angle=NumericValue(value=10, minimum=0, maximum=100, animation=None), target_position=NumericValue(value=10, minimum=0, maximum=100, animation=None), target_angle=NumericValue(value=10, minimum=0, maximum=100, animation=None), system_state=EnumValue(value=ok))"
        )
