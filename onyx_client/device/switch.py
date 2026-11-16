"""Switch class."""

from ..device.device import Device


class Switch(Device):
    """A ONYX controlled switch device."""

    def __str__(self):
        return f"Switch({super().__str__()})"
