"""Tests for the Base Device class."""

import pytest
import pytest_asyncio

from onyx_client.data.device_mode import DeviceMode
from onyx_client.device.device import Device
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType
from onyx_client.exception.update_exception import UpdateException


class TestDevice:
    @pytest_asyncio.fixture
    def device_mode(self):
        yield DeviceMode(DeviceType.ROLLERSHUTTER)

    def test_init(self, device_mode):
        device = Device("id", "name", DeviceType.AWNING, device_mode, list(Action))
        assert device.identifier == "id"
        assert device.device_type == DeviceType.AWNING
        assert device.device_mode.mode == DeviceType.ROLLERSHUTTER

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

    def test_update_with(self, device_mode):
        device = Device("id", "name", DeviceType.AWNING, device_mode, list(Action))
        update = Device(
            "id",
            "name1",
            DeviceType.ROLLERSHUTTER,
            DeviceMode(DeviceType.AWNING),
            [Action.STOP],
        )
        device.update_with(update)
        assert device.name == "name1"
        assert device.device_type == DeviceType.ROLLERSHUTTER
        assert device.device_mode.mode == DeviceType.AWNING
        assert Action.STOP in device.actions

    def test_update_with_none(self, device_mode):
        device = Device("id", "name", DeviceType.AWNING, device_mode, list(Action))
        update = Device("id", None, None, None, None)
        device.update_with(update)
        assert device.name == "name"
        assert device.device_type == DeviceType.AWNING
        assert device.device_mode.mode == DeviceType.ROLLERSHUTTER
        assert device.actions == list(Action)

    def test_update_with_exception(self, device_mode):
        device = Device("id", "name", DeviceType.AWNING, device_mode, list(Action))
        update = Device(
            "other",
            "name1",
            DeviceType.ROLLERSHUTTER,
            DeviceMode(DeviceType.AWNING),
            [Action.STOP],
        )
        with pytest.raises(UpdateException):
            device.update_with(update)
