"""Device class."""
from onyx_client.data.device_mode import DeviceMode
from onyx_client.enum.device_type import DeviceType


class Device:
    """A ONYX controlled device."""

    def __init__(
        self,
        identifier: str,
        name: str,
        device_type: DeviceType,
        device_mode: DeviceMode,
        actions: list,
    ):
        """Initialize the device."""
        self.identifier = identifier
        self.name = name
        self.device_type = device_type
        self.device_mode = device_mode
        self.actions = actions

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.identifier == other.identifier
        return False
