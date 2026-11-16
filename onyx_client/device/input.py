"""Input class."""

from ..data.device_mode import DeviceMode
from ..data.enum_value import EnumValue
from ..device.device import Device
from ..enum.device_type import DeviceType


class Input(Device):
    """A wired contact (rain sensor or alarm) connected to an ONYX.NODE."""

    def __init__(
        self,
        identifier: str,
        name: str,
        device_type: DeviceType,
        device_mode: DeviceMode,
        actions: list,
        input_type: EnumValue = None,
        input_active: EnumValue = None,
        **kwargs,
    ):
        """Initialize the input device.

        identifier: the device identifier
        name: the device name
        device_type: the device type
        device_mode: the mode the device can operate as
        actions: a list of actions the device supports
        input_type: the configured role of the contact
        input_active: whether the contact is triggered ("true"/"false")
        kwargs: the optional attributes of Device"""
        super().__init__(identifier, name, device_type, device_mode, actions, **kwargs)
        self.input_type = input_type
        self.input_active = input_active

    def __str__(self):
        return f"Input({super().__str__()}, input_type={self.input_type}, input_active={self.input_active})"
