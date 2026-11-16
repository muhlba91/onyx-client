"""Sun Tag class."""

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
        **kwargs,
    ):
        """Initialize the sun tag.

        identifier: the device identifier
        name: the device name
        device_type: the device type
        device_mode: the mode the device can operate as
        actions: a list of actions the device supports
        sun_brightness: the current brightness
        sun_brightness_peak: the maximum brightness in the last 15 minutes
        sun_brightness_sink: the minimum brightness in the last 15 minutes
        kwargs: the optional attributes of Device"""
        super().__init__(identifier, name, device_type, device_mode, actions, **kwargs)
        self.sun_brightness = sun_brightness
        self.sun_brightness_peak = sun_brightness_peak
        self.sun_brightness_sink = sun_brightness_sink

    def __str__(self):
        return f"TagSun({super().__str__()}, sun_brightness={self.sun_brightness}, sun_brightness_peak={self.sun_brightness_peak}, sun_brightness_sink={self.sun_brightness_sink})"
