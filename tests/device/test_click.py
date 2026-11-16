"""Tests for the Click Device class."""

from onyx_client.data.device_mode import DeviceMode
from onyx_client.device.click import Click
from onyx_client.enum.device_type import DeviceType


class TestClick:
    def test_init(self):
        click = Click(
            "id",
            "name",
            DeviceType.CLICK,
            DeviceMode(DeviceType.CLICK),
            [],
            False,
            tint="#000000",
        )
        assert click.identifier == "id"
        assert click.name == "name"
        assert click.device_type == DeviceType.CLICK
        assert click.device_mode.mode == DeviceType.CLICK
        assert click.actions == []
        assert not click.offline
        assert click.tint == "#000000"

    def test_init_defaults(self):
        click = Click("id", "name", DeviceType.CLICK, None, [])
        assert click.offline

    def test_str(self):
        assert (
            str(Click("id", "name", DeviceType.CLICK, None, [], False))
            == "Click(Device(id=id, name=name, type=DeviceType.CLICK), offline=False)"
        )
