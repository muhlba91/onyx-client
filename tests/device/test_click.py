"""Tests for the Click Device class."""

import pytest
import pytest_asyncio

from onyx_client.data.device_mode import DeviceMode
from onyx_client.device.click import Click
from onyx_client.device.device import Device
from onyx_client.enum.device_type import DeviceType
from onyx_client.exception.update_exception import UpdateException


class TestClick:
    @pytest_asyncio.fixture
    def device_mode(self):
        yield DeviceMode(DeviceType.CLICK)

    def test_init(self, device_mode):
        click = Click(
            "id",
            "name",
            DeviceType.CLICK,
            False,
        )
        assert click.identifier == "id"
        assert click.name == "name"
        assert click.device_type == DeviceType.CLICK
        assert click.device_mode.mode == DeviceType.CLICK
        assert click.actions == []
        assert not click.offline

    def test_str(self):
        assert (
            str(
                Click(
                    "id",
                    "name",
                    DeviceType.CLICK,
                    False,
                )
            )
            == "Click(Device(id=id, name=name, type=DeviceType.CLICK), offline=False)"
        )

    def test_update_with(self, device_mode):
        click = Click(
            "id",
            "name",
            DeviceType.CLICK,
            False,
        )
        update = Click(
            "id",
            "name1",
            DeviceType.CLICK,
            True,
        )
        click.update_with(update)
        assert click.name == "name1"
        assert click.offline

    def test_update_with_none(self, device_mode):
        click = Click(
            "id",
            "name",
            DeviceType.CLICK,
            False,
        )
        update = Click(
            "id",
            None,
            None,
            None,
        )
        click.update_with(update)
        assert click.name == "name"
        assert not click.offline

    def test_update_with_exception(self, device_mode):
        click = Click(
            "id",
            "name",
            DeviceType.CLICK,
            False,
        )
        update = Click(
            "other",
            None,
            None,
            None,
        )
        with pytest.raises(UpdateException):
            click.update_with(update)

    def test_update_with_base_device_patch(self, device_mode):
        click = Click("id", "name", DeviceType.CLICK, False)
        update = Device(
            "id",
            "patched_name",
            DeviceType.UNKNOWN,
            DeviceMode(DeviceType.UNKNOWN),
            [],
        )
        click.update_with(update)
        assert click.name == "patched_name"
        assert click.device_type == DeviceType.CLICK
        # offline has no attribute on base Device; getattr returns None, so offline keeps original
        assert not click.offline

    def test_keys(self):
        assert Click.keys() == ["offline"]
