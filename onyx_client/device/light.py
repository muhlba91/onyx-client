"""Light class."""

from ..data.device_mode import DeviceMode
from ..data.enum_value import EnumValue
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
        target_hue: NumericValue = None,
        actual_hue: NumericValue = None,
        target_saturation: NumericValue = None,
        actual_saturation: NumericValue = None,
        target_color_temperature: NumericValue = None,
        actual_color_temperature: NumericValue = None,
        color_mode: EnumValue = None,
        **kwargs,
    ):
        """Initialize the light device.

        identifier: the device identifier
        name: the device name
        device_type: the device type
        device_mode: the mode the device can operate as
        actions: a list of actions the device supports
        target_brightness: the target brightness of the light
        actual_brightness: the actual brightness of the light
        dim_duration: the duration it takes to dim
        target_hue: the target hue (RGBW only)
        actual_hue: the actual hue (RGBW only)
        target_saturation: the target saturation (RGBW only)
        actual_saturation: the actual saturation (RGBW only)
        target_color_temperature: the target color temperature (RGBW only)
        actual_color_temperature: the actual color temperature (RGBW only)
        color_mode: hsv or temperature (RGBW only)
        kwargs: the optional attributes of Device"""
        super().__init__(identifier, name, device_type, device_mode, actions, **kwargs)
        self.target_brightness = target_brightness
        self.actual_brightness = actual_brightness
        self.dim_duration = dim_duration
        self.target_hue = target_hue
        self.actual_hue = actual_hue
        self.target_saturation = target_saturation
        self.actual_saturation = actual_saturation
        self.target_color_temperature = target_color_temperature
        self.actual_color_temperature = actual_color_temperature
        self.color_mode = color_mode

    def __str__(self):
        return f"Light({super().__str__()}, actual_brightness={self.actual_brightness}, target_brightness={self.target_brightness}, dim_duration={self.dim_duration}, color_mode={self.color_mode})"
