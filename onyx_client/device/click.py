"""Click class."""
from onyx_client.data.device_mode import DeviceMode
from onyx_client.device.device import Device
from onyx_client.enum.device_type import DeviceType


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
        super(Click, self).__init__(
            identifier,
            name,
            device_type,
            DeviceMode(device_type),
            list(),
        )
        self.offline = offline

    def update_with(self, update):
        """Update the device with an update patch.

        update: the update patch"""
        super().update_with(update)

        self.offline = self.offline if update.offline is None else update.offline

    @staticmethod
    def keys() -> list:
        """Get the list of keys specific to the device type."""
        return [
            "offline",
        ]
