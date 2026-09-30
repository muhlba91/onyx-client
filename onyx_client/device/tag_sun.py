"""Sun Tag class."""

from typing import Optional

from ..data.device_mode import DeviceMode
from ..data.numeric_value import NumericValue
from ..device.device import Device
from ..enum.device_type import DeviceType


class TagSun(Device):
    """A ONYX.TAG measuring the sun brightness."""

    def __init__(
        self,
        identifier: str,
        name: str,
        device_type: DeviceType,
        device_mode: DeviceMode,
        actions: list,
        sun_brightness: NumericValue = None,
        sun_brightness_peak: NumericValue = None,
        sun_brightness_sink: NumericValue = None,
    ):
        """Initialize the sun tag.

        identifier: the device identifier
        name: the device name
        device_type: the device type
        actions: a list of actions the device supports
        sun_brightness: the current brightness
        sun_brightness_peak: the maximum brightness in the last 15 minutes
        sun_brightness_sink: the minimum brightness in the last 15 minutes"""
        super().__init__(identifier, name, device_type, device_mode, actions)
        self.sun_brightness = sun_brightness
        self.sun_brightness_peak = sun_brightness_peak
        self.sun_brightness_sink = sun_brightness_sink

    def __str__(self):
        return f"TagSun({super().__str__()}, sun_brightness={self.sun_brightness}, sun_brightness_peak={self.sun_brightness_peak}, sun_brightness_sink={self.sun_brightness_sink})"

    def update_with(self, update: Optional["TagSun"]):
        """Update the device with an update patch.

        update: the update patch"""
        super().update_with(update)

        sun_brightness = getattr(update, "sun_brightness", None)
        if self.sun_brightness is not None:
            self.sun_brightness.update_with(sun_brightness)
        else:
            self.sun_brightness = sun_brightness
        sun_brightness_peak = getattr(update, "sun_brightness_peak", None)
        if self.sun_brightness_peak is not None:
            self.sun_brightness_peak.update_with(sun_brightness_peak)
        else:
            self.sun_brightness_peak = sun_brightness_peak
        sun_brightness_sink = getattr(update, "sun_brightness_sink", None)
        if self.sun_brightness_sink is not None:
            self.sun_brightness_sink.update_with(sun_brightness_sink)
        else:
            self.sun_brightness_sink = sun_brightness_sink

    @staticmethod
    def keys() -> list:
        """Get the list of keys specific to the device type."""
        return [
            "sun_brightness",
            "sun_brightness_peak",
            "sun_brightness_sink",
        ]
