"""Click class."""

from ..data.device_mode import DeviceMode
from ..device.device import Device
from ..enum.device_type import DeviceType


class Click(Device):
    """A ONYX controlled click device."""

    def __init__(
        self,
        identifier: str,
        name: str,
        device_type: DeviceType,
        device_mode: DeviceMode,
        actions: list,
        offline: bool = True,
        **kwargs,
    ):
        """Initialize the click device.

        identifier: the device identifier
        name: the device name
        device_type: the device type
        device_mode: the mode the device can operate as
        actions: a list of actions the device supports
        offline: set if the device is offline
        kwargs: the optional attributes of Device"""
        super().__init__(identifier, name, device_type, device_mode, actions, **kwargs)
        self.offline = offline

    def __str__(self):
        return f"Click({super().__str__()}, offline={self.offline})"
