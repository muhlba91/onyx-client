"""Tests for the CommandSource data class."""

from onyx_client.data.command_source import CommandSource


class TestCommandSource:
    def test_create(self):
        assert CommandSource.create(
            {"type": "automation", "id": "id", "name": "Wind", "emoji": "🌬"}
        ) == CommandSource("automation", "id", "Wind", "🌬")

    def test_create_partial(self):
        assert CommandSource.create({"name": "App User"}) == CommandSource(
            None, None, "App User", None
        )

    def test_create_none(self):
        assert CommandSource.create(None) is None

    def test_str(self):
        assert (
            str(CommandSource("client", None, "App User", None))
            == "CommandSource(type=client, id=None, name=App User)"
        )

    def test_not_eq(self):
        source = CommandSource("automation", "id", "Wind", "🌬")
        assert source != CommandSource("device", "id", "Wind", "🌬")
        assert source != CommandSource("automation", "other", "Wind", "🌬")
        assert source != CommandSource("automation", "id", "Rain", "🌬")
        assert source != CommandSource("automation", "id", "Wind", None)
        assert source != "automation"
