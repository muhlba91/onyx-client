"""Shutter class."""

from ..data.device_mode import DeviceMode
from ..data.enum_value import EnumValue
from ..data.numeric_value import NumericValue
from ..device.device import Device
from ..enum.device_type import DeviceType


class Shutter(Device):
    """A ONYX controlled shutter device."""

    def __init__(
        self,
        identifier: str,
        name: str,
        device_type: DeviceType,
        device_mode: DeviceMode,
        actions: list,
        target_position: NumericValue = None,
        target_angle: NumericValue = None,
        actual_angle: NumericValue = None,
        actual_position: NumericValue = None,
        system_state: EnumValue = None,
        temperature: NumericValue = None,
        humidity: NumericValue = None,
        **kwargs,
    ):
        """Initialize the shutter device.

        identifier: the device identifier
        name: the device name
        device_type: the device type
        device_mode: the mode the device can operate as
        actions: a list of actions the device supports
        target_position: the target position of the shutter
        target_angle: the target angle of the shutter
        actual_position: the actual position of the shutter
        actual_angle: the actual angle of the shutter
        system_state: the calibration and collision state
        temperature: the temperature (in 1/10 degrees Celsius, pergola unit only)
        humidity: the relative humidity (pergola unit only)
        kwargs: the optional attributes of Device"""
        super().__init__(identifier, name, device_type, device_mode, actions, **kwargs)
        self.target_position = target_position
        self.target_angle = target_angle
        self.actual_angle = actual_angle
        self.actual_position = actual_position
        self.system_state = system_state
        self.temperature = temperature
        self.humidity = humidity

    def __str__(self):
        return f"Shutter({super().__str__()}, actual_position={self.actual_position}, actual_angle={self.actual_angle}, target_position={self.target_position}, target_angle={self.target_angle}, system_state={self.system_state})"
