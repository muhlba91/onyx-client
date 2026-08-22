"""Device class."""

from typing import Optional

from ..data.device_mode import DeviceMode
from ..enum.device_type import DeviceType
from ..exception.update_exception import UpdateException


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
        """Initialize the device.

        identifier: the device identifier
        name: the device name
        device_type: the device type
        actions: a list of actions the device supports"""
        self.identifier = identifier
        self.name = name
        self.device_type = device_type
        self.device_mode = device_mode
        self.actions = actions

    def __str__(self):
        return (
            f"Device(id={self.identifier}, name={self.name}, type={self.device_type})"
        )

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.identifier == other.identifier
        return False

    def update_with(self, update: Optional["Device"]):
        """Update the device with an update patch.

        update: the update patch"""
        if update is None or self.identifier != getattr(update, "identifier", None):
            raise UpdateException("ID_NOT_EQUAL")
        self.name = self.name if update.name is None else update.name
        update_device_type = update.device_type
        self.device_type = (
            self.device_type
            if update_device_type is None or update_device_type == DeviceType.UNKNOWN
            else update_device_type
        )
        update_device_mode = update.device_mode
        self.device_mode = (
            self.device_mode
            if update_device_mode is None
            or update_device_mode.mode is None
            or update_device_mode.mode == DeviceType.UNKNOWN
            else update_device_mode
        )
        self.actions = (
            self.actions
            if update.actions is None or len(update.actions) == 0
            else update.actions
        )
