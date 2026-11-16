"""Tests for the Input Device class."""

from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.enum_value import EnumValue
from onyx_client.device.input import Input
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType


class TestInput:
    def test_init(self):
        input_type = EnumValue("rain_sensor", ["rain_sensor", "fire_alarm"], True)
        input_active = EnumValue("true", ["true", "false"], True)
        device = Input(
            "id",
            "name",
            DeviceType.INPUT,
            DeviceMode(DeviceType.INPUT),
            [Action.WINK],
            input_type,
            input_active,
            raw_type="input",
        )
        assert device.identifier == "id"
        assert device.device_type == DeviceType.INPUT
        assert device.actions == [Action.WINK]
        assert device.input_type == input_type
        assert device.input_active.as_bool()
        assert device.raw_type == "input"

    def test_str(self):
        assert (
            str(
                Input(
                    "id",
                    "name",
                    DeviceType.INPUT,
                    None,
                    [],
                    EnumValue("rain_sensor", [], True),
                    EnumValue("false", [], True),
                )
            )
            == "Input(Device(id=id, name=name, type=DeviceType.INPUT), input_type=EnumValue(value=rain_sensor), input_active=EnumValue(value=false))"
        )

    def test_init_common_attributes(self):
        device = Input(
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
