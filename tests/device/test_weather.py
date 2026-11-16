"""Tests for the Weather Device class."""

from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.weather import Weather
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType


class TestWeather:
    def test_init(self):
        values = [NumericValue(index, 0, 100, True) for index in range(8)]
        weather = Weather(
            "id",
            "name",
            DeviceType.WEATHER,
            DeviceMode(DeviceType.WEATHER),
            [Action.WINK],
            *values,
        )
        assert weather.identifier == "id"
        assert weather.name == "name"
        assert weather.device_type == DeviceType.WEATHER
        assert weather.actions == [Action.WINK]
        assert weather.wind_peak == values[0]
        assert weather.sun_brightness_peak == values[1]
        assert weather.sun_brightness_sink == values[2]
        assert weather.air_pressure == values[3]
        assert weather.humidity == values[4]
        assert weather.temperature == values[5]
        assert weather.wind_speed == values[6]
        assert weather.sun_brightness == values[7]

    def test_init_defaults(self):
        weather = Weather("id", "name", DeviceType.WEATHER, None, [])
        assert weather.wind_speed is None
        assert weather.sun_brightness is None

    def test_str(self):
        assert (
            str(Weather("id", "name", DeviceType.WEATHER, None, []))
            == "Weather(Device(id=id, name=name, type=DeviceType.WEATHER), wind_peak=None, wind_speed=None, sun_brightness=None, sun_brightness_peak=None, sun_brightness_sink=None, air_pressure=None, humidity=None, temperature=None)"
        )

    def test_init_common_attributes(self):
        device = Weather(
            "id",
            "name",
            DeviceType.UNKNOWN,
            DeviceMode(DeviceType.UNKNOWN),
            [None],
            tint="#000000",
        )
        assert device.device_mode.mode == DeviceType.UNKNOWN
        assert device.actions == [None]
        assert device.tint == "#000000"
