"""Device class."""

from ..data.active_command import ActiveCommand
from ..data.device_mode import DeviceMode
from ..enum.device_type import DeviceType


class Device:
    """A ONYX controlled device."""

    def __init__(
        self,
        identifier: str,
        name: str,
        device_type: DeviceType,
        device_mode: DeviceMode,
        actions: list,
        raw_type: str | None = None,
        tint: str | None = None,
        active_command: ActiveCommand | None = None,
    ):
        """Initialize the device.

        identifier: the device identifier
        name: the device name
        device_type: the device type
        device_mode: the mode the device can operate as
        actions: a list of actions the device supports
        raw_type: the device type as reported by the API
        tint: the tint color (#RRGGBB)
        active_command: the command the device is currently executing"""
        self.identifier = identifier
        self.name = name
        self.device_type = device_type
        self.device_mode = device_mode
        self.actions = actions
        self.raw_type = raw_type
        self.tint = tint
        self.active_command = active_command

    def __str__(self):
        return (
            f"Device(id={self.identifier}, name={self.name}, type={self.device_type})"
        )

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.identifier == other.identifier
        return False
