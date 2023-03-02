"""Tests for the Switch Device class."""
import pytest
import pytest_asyncio

from onyx_client.data.device_mode import DeviceMode
from onyx_client.device.switch import Switch
from onyx_client.enum.device_type import DeviceType
from onyx_client.exception.update_exception import UpdateException


class TestSwitch:
    @pytest_asyncio.fixture
    def device_mode(self):
        yield DeviceMode(DeviceType.SWITCH)

    def test_init(self, device_mode):
        switch = Switch(
            "id",
            "name",
            DeviceType.SWITCH,
        )
        assert switch.identifier == "id"
        assert switch.device_type == DeviceType.SWITCH
        assert switch.device_mode.mode == DeviceType.SWITCH

    def test_update_with(self, device_mode):
        switch = Switch(
            "id",
            "name",
            DeviceType.SWITCH,
        )
        update = Switch(
            "id",
            "name1",
            DeviceType.SWITCH,
        )
        switch.update_with(update)
        assert switch.name == "name1"

    def test_update_with_none(self, device_mode):
        switch = Switch(
            "id",
            "name",
            DeviceType.SWITCH,
        )
        update = Switch(
            "id",
            None,
            None,
        )
        switch.update_with(update)
        assert switch.name == "name"

    def test_update_with_exception(self, device_mode):
        switch = Switch(
            "id",
            "name",
            DeviceType.CLICK,
        )
        update = Switch(
            "other",
            None,
            None,
        )
        with pytest.raises(UpdateException):
            switch.update_with(update)
