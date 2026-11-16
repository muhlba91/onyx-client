"""Tests for the CommandAttribute enum."""

from onyx_client.enum.command_attribute import CommandAttribute


class TestCommandAttribute:
    def test_convert(self):
        assert CommandAttribute.convert("silent") == CommandAttribute.SILENT

    def test_convert_invalid(self):
        assert CommandAttribute.convert("foo") is None
        assert CommandAttribute.convert(None) is None

    def test_string(self):
        assert CommandAttribute.URGENT.string() == "urgent"
