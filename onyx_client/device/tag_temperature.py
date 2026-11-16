"""Temperature Tag class."""

from ..data.device_mode import DeviceMode
from ..data.numeric_value import NumericValue
from ..device.device import Device
from ..enum.device_type import DeviceType


class TagTemperature(Device):
    """A ONYX.TAG measuring temperature and humidity."""

    def __init__(
        self,
        identifier: str,
        name: str,
        device_type: DeviceType,
        device_mode: DeviceMode,
        actions: list,
        temperature: NumericValue = None,
        humidity: NumericValue = None,
        **kwargs,
    ):
        """Initialize the temperature tag.

        identifier: the device identifier
        name: the device name
        device_type: the device type
        device_mode: the mode the device can operate as
        actions: a list of actions the device supports
        temperature: the temperature (in 1/10 degrees Celsius)
        humidity: the relative humidity
        kwargs: the optional attributes of Device"""
        super().__init__(identifier, name, device_type, device_mode, actions, **kwargs)
        self.temperature = temperature
        self.humidity = humidity

    def __str__(self):
        return f"TagTemperature({super().__str__()}, temperature={self.temperature}, humidity={self.humidity})"
