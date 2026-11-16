"""Tests for the Switch Device class."""

from onyx_client.data.device_mode import DeviceMode
from onyx_client.device.switch import Switch
from onyx_client.enum.device_type import DeviceType


class TestSwitch:
    def test_init(self):
        switch = Switch(
            "id", "name", DeviceType.SWITCH, DeviceMode(DeviceType.SWITCH), []
        )
        assert switch.identifier == "id"
        assert switch.name == "name"
        assert switch.device_type == DeviceType.SWITCH
        assert switch.device_mode.mode == DeviceType.SWITCH

    def test_str(self):
        assert (
            str(Switch("id", "name", DeviceType.SWITCH, None, []))
            == "Switch(Device(id=id, name=name, type=DeviceType.SWITCH))"
        )
