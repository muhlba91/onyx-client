"""Switch class."""
from onyx_client.data.device_mode import DeviceMode
from onyx_client.device.device import Device
from onyx_client.enum.device_type import DeviceType


class Switch(Device):
    """A ONYX controlled switch device."""

    def __init__(self, identifier: str, name: str, device_type: DeviceType):
        """Initialize the switch device."""
        super(Switch, self).__init__(
            identifier,
            name,
            device_type,
            DeviceMode(device_type),
            list(),
        )

    def update_with(self, update):
        super().update_with(update)

    @staticmethod
    def keys() -> list:
        return []
