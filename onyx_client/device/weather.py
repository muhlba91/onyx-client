"""Weather class."""

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
        wind_speed: NumericValue = None,
        sun_brightness: NumericValue = None,
        **kwargs,
    ):
        """Initialize the weather device.

        identifier: the device identifier
        name: the device name
        device_type: the device type
        device_mode: the mode the device can operate as
        actions: a list of actions the device supports
        wind_peak: the maximum wind speed in the last 15 minutes
        sun_brightness_peak: the maximum brightness in the last 15 minutes
        sun_brightness_sink: the minimum brightness in the last 15 minutes
        air_pressure: the absolute air pressure
        humidity: the relative humidity
        temperature: the temperature of the station
        wind_speed: the current wind speed
        sun_brightness: the brightness of the last measurement
        kwargs: the optional attributes of Device"""
        super().__init__(identifier, name, device_type, device_mode, actions, **kwargs)
        self.wind_peak = wind_peak
        self.sun_brightness_peak = sun_brightness_peak
        self.sun_brightness_sink = sun_brightness_sink
        self.air_pressure = air_pressure
        self.humidity = humidity
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.sun_brightness = sun_brightness

    def __str__(self):
        return f"Weather({super().__str__()}, wind_peak={self.wind_peak}, wind_speed={self.wind_speed}, sun_brightness={self.sun_brightness}, sun_brightness_peak={self.sun_brightness_peak}, sun_brightness_sink={self.sun_brightness_sink}, air_pressure={self.air_pressure}, humidity={self.humidity}, temperature={self.temperature})"
