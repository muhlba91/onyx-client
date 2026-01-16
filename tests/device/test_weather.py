"""Tests for the Weather Device class."""

import pytest
import pytest_asyncio

from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.weather import Weather
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType
from onyx_client.exception.update_exception import UpdateException


class TestWeather:
    @pytest_asyncio.fixture
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

    def test_str(self):
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
            None,
            list(Action),
            value1,
            value2,
            value3,
            value4,
            value5,
            value6,
        )
        assert (
            str(weather)
            == "Weather(Device(id=id, name=name, type=DeviceType.WEATHER), wind_peak=NumericValue(value=1, minimum=0, maximum=10, animation=None), sun_brightness_peak=NumericValue(value=2, minimum=0, maximum=10, animation=None), sun_brightness_sink=NumericValue(value=3, minimum=0, maximum=10, animation=None), air_pressure=NumericValue(value=4, minimum=0, maximum=10, animation=None), humidity=NumericValue(value=5, minimum=0, maximum=10, animation=None), temperature=NumericValue(value=6, minimum=0, maximum=10, animation=None))"
        )

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

    def test_update_with(self, device_mode):
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
        update = Weather(
            "id",
            "name1",
            DeviceType.WEATHER,
            device_mode,
            list(Action),
            value6,
            value5,
            value4,
            value3,
            value2,
            value1,
        )
        weather.update_with(update)
        assert weather.name == "name1"
        assert weather.wind_peak == value6
        assert weather.sun_brightness_peak == value5
        assert weather.sun_brightness_sink == value4
        assert weather.air_pressure == value3
        assert weather.humidity == value2
        assert weather.temperature == value1

    def test_update_with_no_data_update_data(self, device_mode):
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
            None,
            None,
            None,
            None,
            None,
            None,
        )
        update = Weather(
            "id",
            "name1",
            DeviceType.WEATHER,
            device_mode,
            list(Action),
            value6,
            value5,
            value4,
            value3,
            value2,
            value1,
        )
        weather.update_with(update)
        assert weather.name == "name1"
        assert weather.wind_peak == value6
        assert weather.sun_brightness_peak == value5
        assert weather.sun_brightness_sink == value4
        assert weather.air_pressure == value3
        assert weather.humidity == value2
        assert weather.temperature == value1

    def test_update_with_no_data_update_none(self, device_mode):
        weather = Weather(
            "id",
            "name",
            DeviceType.WEATHER,
            device_mode,
            list(Action),
            None,
            None,
            None,
            None,
            None,
            None,
        )
        update = Weather(
            "id",
            "name1",
            DeviceType.WEATHER,
            device_mode,
            list(Action),
            None,
            None,
            None,
            None,
            None,
            None,
        )
        weather.update_with(update)
        assert weather.name == "name1"
        assert weather.wind_peak is None
        assert weather.sun_brightness_peak is None
        assert weather.sun_brightness_sink is None
        assert weather.air_pressure is None
        assert weather.humidity is None
        assert weather.temperature is None

    def test_update_with_none(self, device_mode):
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
        update = Weather(
            "id",
            None,
            None,
            None,
            None,
        )
        weather.update_with(update)
        assert weather.name == "name"
        assert weather.wind_peak == value1
        assert weather.sun_brightness_peak == value2
        assert weather.sun_brightness_sink == value3
        assert weather.air_pressure == value4
        assert weather.humidity == value5
        assert weather.temperature == value6

    def test_update_with_exception(self, device_mode):
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
        update = Weather(
            "other",
            None,
            None,
            None,
            None,
        )
        with pytest.raises(UpdateException):
            weather.update_with(update)

    def test_update_with_partials(self, device_mode):
        value1 = NumericValue(1, 0, 10, False)
        value2 = NumericValue(2, 0, 10, False)
        value3 = NumericValue(3, 0, 10, False)
        value4 = NumericValue(4, 0, 10, False)
        value5 = NumericValue(5, 0, 10, False)
        value6 = NumericValue(6, 0, 10, False)
        value7 = NumericValue(10, None, None, False)
        value8 = NumericValue(None, 10, None, False)
        value9 = NumericValue(None, None, 100, False)
        value10 = NumericValue(40, None, None, False)
        value11 = NumericValue(None, 10, None, False)
        value12 = NumericValue(None, None, 100, False)
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
        update = Weather(
            "id",
            "name1",
            DeviceType.WEATHER,
            device_mode,
            list(Action),
            value7,
            value8,
            value9,
            value10,
            value11,
            value12,
        )
        weather.update_with(update)
        assert weather.name == "name1"
        assert weather.wind_peak == NumericValue(10, 0, 10, False)
        assert weather.sun_brightness_peak == NumericValue(2, 10, 10, False)
        assert weather.sun_brightness_sink == NumericValue(3, 0, 100, False)
        assert weather.air_pressure == NumericValue(40, 0, 10, False)
        assert weather.humidity == NumericValue(5, 10, 10, False)
        assert weather.temperature == NumericValue(6, 0, 100, False)
