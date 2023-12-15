"""Switch class."""
from typing import Optional

from ..data.device_mode import DeviceMode
from ..device.device import Device
from ..enum.device_type import DeviceType


class Switch(Device):
    """A ONYX controlled switch device."""

    def __init__(self, identifier: str, name: str, device_type: DeviceType):
        """Initialize the switch device.

        identifier: the device identifier
        name: the device name
        device_type: the device type"""
        super(Switch, self).__init__(
            identifier,
            name,
            device_type,
            DeviceMode(device_type),
            list(),
        )

    def update_with(self, update: Optional["Switch"]):
        """Update the device with an update patch.

        update: the update patch"""
        super().update_with(update)

    def __str__(self):
        return f"Switch({super().__str__()})"

    @staticmethod
    def keys() -> list:
        """Get the list of keys specific to the device type."""
        return []
