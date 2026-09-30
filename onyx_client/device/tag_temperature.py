"""Temperature Tag class."""

from typing import Optional

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
    ):
        """Initialize the temperature tag.

        identifier: the device identifier
        name: the device name
        device_type: the device type
        actions: a list of actions the device supports
        temperature: the temperature (in 1/10 degrees Celsius)
        humidity: the relative humidity"""
        super().__init__(identifier, name, device_type, device_mode, actions)
        self.temperature = temperature
        self.humidity = humidity

    def __str__(self):
        return f"TagTemperature({super().__str__()}, temperature={self.temperature}, humidity={self.humidity})"

    def update_with(self, update: Optional["TagTemperature"]):
        """Update the device with an update patch.

        update: the update patch"""
        super().update_with(update)

        temperature = getattr(update, "temperature", None)
        if self.temperature is not None:
            self.temperature.update_with(temperature)
        else:
            self.temperature = temperature
        humidity = getattr(update, "humidity", None)
        if self.humidity is not None:
            self.humidity.update_with(humidity)
        else:
            self.humidity = humidity

    @staticmethod
    def keys() -> list:
        """Get the list of keys specific to the device type."""
        return [
            "temperature",
            "humidity",
        ]
