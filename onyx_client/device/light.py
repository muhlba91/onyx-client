"""Light class."""
from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.device import Device
from onyx_client.enum.device_type import DeviceType


class Light(Device):
    """A ONYX controlled light."""

    def __init__(
        self,
        identifier: str,
        name: str,
        device_type: DeviceType,
        device_mode: DeviceMode,
        actions: list,
        target_brightness: NumericValue = None,
        actual_brightness: NumericValue = None,
        dim_duration: NumericValue = None,
    ):
        """Initialize the light device."""
        super(Light, self).__init__(identifier, name, device_type, device_mode, actions)
        self.target_brightness = target_brightness
        self.actual_brightness = actual_brightness
        self.dim_duration = dim_duration

    def update_with(self, update):
        super().update_with(update)

        self.target_brightness = (
            self.target_brightness
            if update.target_brightness is None
            else update.target_brightness
        )
        self.actual_brightness = (
            self.actual_brightness
            if update.actual_brightness is None
            else update.actual_brightness
        )
        self.dim_duration = (
            self.dim_duration if update.dim_duration is None else update.dim_duration
        )

    @staticmethod
    def keys() -> list:
        return [
            "target_brightness",
            "actual_brightness",
            "dim_duration",
        ]
