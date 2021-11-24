"""Device Types of Onyx devices."""
from enum import Enum, auto


class DeviceType(Enum):
    """The device types supported by Onyx."""

    ROLLERSHUTTER = auto()
    AWNING = auto()
    RAFFSTORE_90 = auto()
    RAFFSTORE_180 = auto()
    WEATHER = auto()
    VENEER = auto()
    BASIC_LIGHT = auto()
    CLICK = auto()
    SWITCH = auto()
    UNKNOWN = 9999

    def string(self) -> str:
        """Get the string representation for the Onyx API."""
        return self.name.lower()

    def is_shutter(self) -> bool:
        """Check if the type corresponds to any kind of shutter."""
        return self in [
            self.ROLLERSHUTTER,
            self.AWNING,
            self.RAFFSTORE_90,
            self.RAFFSTORE_180,
        ]

    @staticmethod
    def convert(lower: str):
        """Get the device type from the Onyx API's type information."""
        try:
            return DeviceType[lower.upper()]
        except (KeyError, AttributeError):
            return None
