"""Active Command of an Onyx device."""

from ..data.command_source import CommandSource
from ..enum.action import Action
from ..enum.command_attribute import CommandAttribute


class ActiveCommand:
    """The command a device is currently executing."""

    def __init__(
        self,
        source: CommandSource | None,
        action: Action | None,
        properties: dict | None,
        attributes: list,
        valid_from: int | None,
        best_before: int | None,
        active_indicators: list,
    ):
        """Initialize the active command.

        source: the source of the command
        action: the action of the command
        properties: the properties of the command
        attributes: the command attributes
        valid_from: the start of the command validity
        best_before: the deadline of the command validity
        active_indicators: free-form tags why the command is active"""
        self.source = source
        self.action = action
        self.properties = properties
        self.attributes = attributes
        self.valid_from = valid_from
        self.best_before = best_before
        self.active_indicators = active_indicators

    def __str__(self) -> str:
        return f"ActiveCommand(source={self.source}, action={self.action}, properties={self.properties}, best_before={self.best_before})"

    @staticmethod
    def create(properties: dict):
        """Create an active command from properties.

        properties: the properties of the command"""
        if properties is None:
            return None

        return ActiveCommand(
            CommandSource.create(properties.get("source")),
            Action.convert(properties.get("action")),
            properties.get("properties"),
            [
                CommandAttribute.convert(attribute)
                for attribute in properties.get("attributes") or []
            ],
            properties.get("valid_from"),
            properties.get("best_before"),
            properties.get("active_indicators") or [],
        )

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.source == other.source
                and self.action == other.action
                and self.properties == other.properties
                and self.attributes == other.attributes
                and self.valid_from == other.valid_from
                and self.best_before == other.best_before
                and self.active_indicators == other.active_indicators
            )
        return False
