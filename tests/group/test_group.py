"""Tests for the Group class."""
from onyx_client.group.group import Group


class TestGroup:
    def test_init(self):
        group = Group("id", "name", ["device"])
        assert group.identifier == "id"
        assert "device" in group.devices

    def test_eq(self):
        assert Group("id", "name", ["device"]) == Group("id", "name1", ["device"])

    def test_not_eq(self):
        assert Group("id", "name", ["device"]) != 10
