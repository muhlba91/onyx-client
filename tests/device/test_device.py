"""Tests for the Base Device class."""

import pytest_asyncio

from onyx_client.data.active_command import ActiveCommand
from onyx_client.data.device_mode import DeviceMode
from onyx_client.device.device import Device
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType


class TestDevice:
    @pytest_asyncio.fixture
    def device_mode(self):
        yield DeviceMode(DeviceType.ROLLERSHUTTER)

    def test_init(self, device_mode):
        device = Device("id", "name", DeviceType.AWNING, device_mode, list(Action))
        assert device.identifier == "id"
        assert device.name == "name"
        assert device.device_type == DeviceType.AWNING
        assert device.device_mode.mode == DeviceType.ROLLERSHUTTER
        assert device.actions == list(Action)
        assert device.raw_type is None
        assert device.tint is None
        assert device.active_command is None

    def test_init_optional(self, device_mode):
        command = ActiveCommand(None, Action.STOP, None, [], None, None, [])
        device = Device(
            "id",
            "name",
            DeviceType.UNKNOWN,
            device_mode,
            [],
            raw_type="new_type",
            tint="#FFFFFF",
            active_command=command,
        )
        assert device.raw_type == "new_type"
        assert device.tint == "#FFFFFF"
        assert device.active_command == command

    def test_str(self, device_mode):
        assert (
            str(Device("id", "name", DeviceType.AWNING, device_mode, list(Action)))
            == "Device(id=id, name=name, type=DeviceType.AWNING)"
        )

    def test_eq(self, device_mode):
        assert Device(
            "id", "name", DeviceType.AWNING, device_mode, list(Action)
        ) == Device("id", "name1", DeviceType.AWNING, device_mode, list(Action))

    def test_not_eq(self, device_mode):
        assert Device("id", "name", DeviceType.AWNING, device_mode, list(Action)) != 10
        assert Device(
            "id", "name", DeviceType.AWNING, device_mode, list(Action)
        ) != Device("other_id", "name", DeviceType.AWNING, device_mode, list(Action))
