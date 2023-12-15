"""Light class."""
from typing import Optional

from ..data.device_mode import DeviceMode
from ..data.numeric_value import NumericValue
from ..device.device import Device
from ..enum.device_type import DeviceType


class Light(Device):
    """A ONYX controlled light."""

    def __init__(
        self,
        identifier: str,
        name: str,
        device_type: DeviceType,
        device_mode: DeviceMode,
        actions: list,
        target_brightness: NumericValue = None,
        actual_brightness: NumericValue = None,
        dim_duration: NumericValue = None,
    ):
        """Initialize the light device.

        identifier: the device identifier
        name: the device name
        device_type: the device type
        device_mode: the mode the device can operate as
        actions: a list of actions the device supports
        target_brightness: the target brightness of the light
        actual_brightness: the actual brightness of the light
        dim_duration: the duration it takes to dim"""
        super(Light, self).__init__(identifier, name, device_type, device_mode, actions)
        self.target_brightness = target_brightness
        self.actual_brightness = actual_brightness
        self.dim_duration = dim_duration

    def __str__(self):
        return f"Light({super().__str__()}, actual_brightness={self.actual_brightness}, target_brightness={self.target_brightness}, dim_duration={self.dim_duration})"

    def update_with(self, update: Optional["Light"]):
        """Update the device with a patch.

        update: the update patch"""
        super().update_with(update)

        if self.target_brightness is not None:
            self.target_brightness.update_with(update.target_brightness)
        else:
            self.target_brightness = update.target_brightness
        self.actual_brightness.update_with(update.actual_brightness)
        self.dim_duration.update_with(update.dim_duration)

    @staticmethod
    def keys() -> list:
        """Get the list of keys specific to the device type."""
        return [
            "target_brightness",
            "actual_brightness",
            "dim_duration",
        ]
