"""Tests for the Action enum."""

from onyx_client.enum.action import Action


class TestAction:
    def test_convert(self):
        assert Action.convert(Action.STOP.name.lower()) == Action.STOP

    def test_convert_invalid(self):
        assert not Action.convert("foo")

    def test_string(self):
        assert Action.STOP.string() == "stop"
