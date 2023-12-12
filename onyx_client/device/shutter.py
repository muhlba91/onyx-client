"""Shutter class."""
from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.device import Device
from onyx_client.enum.device_type import DeviceType


# not mapped properties:
# - auto_calibration
# - heart_beat_enabled
# - sun_guard_lower_action
# - sun_guard_lower_angle
# - sun_guard_lower_position
# - sun_guard_lower_threshold
# - sun_guard_upper_action
# - sun_guard_upper_angle
# - sun_guard_upper_position
# - sun_guard_upper_threshold
# - system_state
# - wind_guard_enabled
# - wind_peak_threshold
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
        actual_angle: the actual angle of the shutter"""
        super(Shutter, self).__init__(
            identifier, name, device_type, device_mode, actions
        )
        self.target_position = target_position
        self.target_angle = target_angle
        self.actual_angle = actual_angle
        self.actual_position = actual_position

    def __str__(self):
        return f"Shutter({super().__str__()}, actual_position={self.actual_position}, actual_angle={self.actual_angle}, target_position={self.target_position}, target_angle={self.target_angle})"

    def update_with(self, update):
        """Update the device with an update patch.

        update: the update patch"""
        super().update_with(update)

        self.target_position = (
            self.target_position
            if update.target_position is None
            else update.target_position
        )
        self.target_angle = (
            self.target_angle if update.target_angle is None else update.target_angle
        )
        self.actual_angle.update_with(update.actual_angle)
        self.actual_position.update_with(update.actual_position)

    @staticmethod
    def keys() -> list:
        """Get the list of keys specific to the device type."""
        return [
            "target_position",
            "target_angle",
            "actual_angle",
            "actual_position",
        ]
