"""Tests for the ActiveCommand data class."""

from onyx_client.data.active_command import ActiveCommand
from onyx_client.data.command_source import CommandSource
from onyx_client.enum.action import Action
from onyx_client.enum.command_attribute import CommandAttribute


class TestActiveCommand:
    def test_create(self):
        assert ActiveCommand.create(
            {
                "source": {"type": "automation", "id": "id", "name": "Wind"},
                "properties": {"target_position": 0},
                "attributes": ["fast"],
                "valid_from": 1527510327,
                "best_before": 1527510900,
                "active_indicators": ["wind"],
            }
        ) == ActiveCommand(
            CommandSource("automation", "id", "Wind", None),
            None,
            {"target_position": 0},
            [CommandAttribute.FAST],
            1527510327,
            1527510900,
            ["wind"],
        )

    def test_create_action(self):
        command = ActiveCommand.create({"action": "stop", "best_before": 1})
        assert command == ActiveCommand(None, Action.STOP, None, [], None, 1, [])

    def test_create_none(self):
        assert ActiveCommand.create(None) is None

    def test_str(self):
        assert (
            str(ActiveCommand(None, Action.STOP, None, [], None, 1, []))
            == "ActiveCommand(source=None, action=Action.STOP, properties=None, best_before=1)"
        )

    def test_not_eq(self):
        command = ActiveCommand(None, Action.STOP, {}, [], 0, 1, [])
        assert command != ActiveCommand(
            CommandSource(None, None, None, None), Action.STOP, {}, [], 0, 1, []
        )
        assert command != ActiveCommand(None, Action.OPEN, {}, [], 0, 1, [])
        assert command != ActiveCommand(None, Action.STOP, None, [], 0, 1, [])
        assert command != ActiveCommand(
            None, Action.STOP, {}, [CommandAttribute.FAST], 0, 1, []
        )
        assert command != ActiveCommand(None, Action.STOP, {}, [], 1, 1, [])
        assert command != ActiveCommand(None, Action.STOP, {}, [], 0, 2, [])
        assert command != ActiveCommand(None, Action.STOP, {}, [], 0, 1, ["wind"])
        assert command != "stop"
