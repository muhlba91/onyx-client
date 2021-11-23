"""Click class."""
from onyx_client.data.device_mode import DeviceMode
from onyx_client.device.device import Device
from onyx_client.enum.device_type import DeviceType


class Click(Device):
    """A ONYX controlled click device."""

    def __init__(
        self, identifier: str, name: str, device_type: DeviceType, offline: bool
    ):
        """Initialize the click device."""
        super(Click, self).__init__(
            identifier,
            name,
            device_type,
            DeviceMode(device_type),
            list(),
        )
        self.offline = offline

    def update_with(self, update):
        super().update_with(update)

        self.offline = self.offline if update.offline is None else update.offline

    @staticmethod
    def keys() -> list:
        return [
            "offline",
        ]
