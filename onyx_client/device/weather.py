"""Weather class."""
from typing import Optional

from ..data.device_mode import DeviceMode
from ..data.numeric_value import NumericValue
from ..device.device import Device
from ..enum.device_type import DeviceType


class Weather(Device):
    """A ONYX controlled weather station."""

    def __init__(
        self,
        identifier: str,
        name: str,
        device_type: DeviceType,
        device_mode: DeviceMode,
        actions: list,
        wind_peak: NumericValue = None,
        sun_brightness_peak: NumericValue = None,
        sun_brightness_sink: NumericValue = None,
        air_pressure: NumericValue = None,
        humidity: NumericValue = None,
        temperature: NumericValue = None,
    ):
        """Initialize the weather device.

        identifier: the device identifier
        name: the device name
        device_type: the device type
        actions: a list of actions the device supports
        wind_peak: the maximum wind speed in the last 15 minutes
        sun_brightness_peak: the maximum brightness in the last 15 minutes
        sun_brightness_sink: the minimum brightness in the last 15 minutes
        air_pressure: the absolute air pressure
        humidity: the relative humidity
        temperature: the temperature of the station"""
        super(Weather, self).__init__(
            identifier, name, device_type, device_mode, actions
        )
        self.wind_peak = wind_peak
        self.sun_brightness_peak = sun_brightness_peak
        self.sun_brightness_sink = sun_brightness_sink
        self.air_pressure = air_pressure
        self.humidity = humidity
        self.temperature = temperature

    def __str__(self):
        return f"Weather({super().__str__()}, wind_peak={self.wind_peak}, sun_brightness_peak={self.sun_brightness_peak}, sun_brightness_sink={self.sun_brightness_sink}, air_pressure={self.air_pressure}, humidity={self.humidity}, temperature={self.temperature})"

    def update_with(self, update: Optional["Weather"]):
        """Update the device with an update patch.

        update: the update patch"""
        super().update_with(update)

        self.wind_peak.update_with(update.wind_peak)
        self.sun_brightness_peak.update_with(update.sun_brightness_peak)
        self.sun_brightness_sink.update_with(update.sun_brightness_sink)
        self.air_pressure.update_with(update.air_pressure)
        self.humidity.update_with(update.humidity)
        self.temperature.update_with(update.temperature)

    @staticmethod
    def keys() -> list:
        """Get the list of keys specific to the device type."""
        return [
            "wind_peak",
            "sun_brightness_peak",
            "sun_brightness_sink",
            "air_pressure",
            "humidity",
            "temperature",
        ]
