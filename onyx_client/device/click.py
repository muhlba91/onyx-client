"""Click class."""

from ..data.device_mode import DeviceMode
from ..device.device import Device
from ..enum.device_type import DeviceType


class Click(Device):
    """A ONYX controlled click device."""

    def __init__(
        self, identifier: str, name: str, device_type: DeviceType, offline: bool
    ):
        """Initialize the click device.

        identifier: the device identifier
        name: the device name
        device_type: the device type
        offline: set if the device is offline"""
        super().__init__(
            identifier,
            name,
            device_type,
            DeviceMode(device_type),
            [],
        )
        self.offline = offline

    def __str__(self):
        return f"Click({super().__str__()}, offline={self.offline})"

    def update_with(self, update):
        """Update the device with an update patch.

        update: the update patch"""
        super().update_with(update)

        offline = getattr(update, "offline", None)
        self.offline = self.offline if offline is None else offline

    @staticmethod
    def keys() -> list:
        """Get the list of keys specific to the device type."""
        return [
            "offline",
        ]
