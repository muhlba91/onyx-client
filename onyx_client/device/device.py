"""Device class."""
from onyx_client.data.device_mode import DeviceMode
from onyx_client.enum.device_type import DeviceType
from onyx_client.exception.update_exception import UpdateException


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

    def update_with(self, update):
        if not self == update:
            raise UpdateException("ID_NOT_EQUAL")
        self.name = self.name if update.name is None else update.name
        self.device_type = (
            self.device_type if update.device_type is None else update.device_type
        )
        self.device_mode = (
            self.device_mode if update.device_mode is None else update.device_mode
        )
        self.actions = (
            self.actions
            if update.actions is None or len(update.actions) == 0
            else update.actions
        )
