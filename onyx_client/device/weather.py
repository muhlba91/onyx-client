"""Weather class."""
from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.device import Device
from onyx_client.enum.device_type import DeviceType


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

    def update_with(self, update):
        """Update the device with an update patch.

        update: the update patch"""
        super().update_with(update)

        self.wind_peak = (
            self.wind_peak if update.wind_peak is None else update.wind_peak
        )
        self.sun_brightness_peak = (
            self.sun_brightness_peak
            if update.sun_brightness_peak is None
            else update.sun_brightness_peak
        )
        self.sun_brightness_sink = (
            self.sun_brightness_sink
            if update.sun_brightness_sink is None
            else update.sun_brightness_sink
        )
        self.air_pressure = (
            self.air_pressure if update.air_pressure is None else update.air_pressure
        )
        self.humidity = self.humidity if update.humidity is None else update.humidity
        self.temperature = (
            self.temperature if update.temperature is None else update.temperature
        )

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
