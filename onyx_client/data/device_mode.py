"""Device Mode for an Onyx device."""
from onyx_client.enum.device_type import DeviceType


class DeviceMode:
    """The device mode for the device."""

    def __init__(self, mode: DeviceType, values: list = None):
        """Initialize the device mode."""
        self.mode = mode
        self.values = values
