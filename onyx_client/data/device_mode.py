"""Device Mode for an Onyx device."""

from ..enum.device_type import DeviceType


class DeviceMode:
    """The device mode for the device."""

    def __init__(self, mode: DeviceType, values: list = None):
        """Initialize the device mode.

        mode: the device type
        values: a list of valid values"""
        self.mode = mode
        self.values = values
