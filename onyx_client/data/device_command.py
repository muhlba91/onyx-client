"""Device Command for an Onyx device."""
from onyx_client.enum.action import Action
from onyx_client.exception.invalid_command import InvalidCommandException


class DeviceCommand:
    """The representation of a device command."""

    def __init__(
        self,
        properties: dict = None,
        action: Action = None,
        valid_from: int = None,
        best_before: int = None,
    ):
        """Initialize the command."""
        if (properties is None and action is None) or (
            properties is not None and action is not None
        ):
            raise InvalidCommandException("COMMAND_NO_PROPERTIES_OR_ACTION")

        self.properties = properties
        self.action = action
        self.valid_from = valid_from
        self.best_before = best_before

    def data(self) -> dict:
        """Get the dict representation."""
        data = {}
        if self.properties is not None:
            data = {**data, "properties": {**self.properties}}
        if self.action is not None:
            data = {**data, "action": self.action.name.lower()}
        if self.valid_from is not None:
            data = {**data, "valid_from": self.valid_from}
        if self.best_before is not None:
            data = {**data, "best_before": self.best_before}
        return data
