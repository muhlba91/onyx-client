"""Tests for the Weather Device class."""
import pytest

from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.weather import Weather
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType


class TestWeather:
    @pytest.fixture
    def device_mode(self):
        yield DeviceMode(DeviceType.WEATHER)

    def test_init(self, device_mode):
        value1 = NumericValue(1, 0, 10, False)
        value2 = NumericValue(2, 0, 10, False)
        value3 = NumericValue(3, 0, 10, False)
        value4 = NumericValue(4, 0, 10, False)
        value5 = NumericValue(5, 0, 10, False)
        value6 = NumericValue(6, 0, 10, False)
        weather = Weather(
            "id",
            "name",
            DeviceType.WEATHER,
            device_mode,
            list(Action),
            value1,
            value2,
            value3,
            value4,
            value5,
            value6,
        )
        assert weather.identifier == "id"
        assert weather.device_type == DeviceType.WEATHER
        assert weather.device_mode.mode == DeviceType.WEATHER
        assert weather.wind_peak == value1
        assert weather.sun_brightness_peak == value2
        assert weather.sun_brightness_sink == value3
        assert weather.air_pressure == value4
        assert weather.humidity == value5
        assert weather.temperature == value6

    def test_init_no_additional_values(self, device_mode):
        weather = Weather(
            "id",
            "name",
            DeviceType.WEATHER,
            device_mode,
            list(Action),
        )
        assert weather.identifier == "id"
        assert weather.device_type == DeviceType.WEATHER
        assert weather.device_mode.mode == DeviceType.WEATHER
        assert weather.wind_peak is None
        assert weather.sun_brightness_peak is None
        assert weather.sun_brightness_sink is None
        assert weather.air_pressure is None
        assert weather.humidity is None
        assert weather.temperature is None
