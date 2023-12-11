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
    PERGOLA_AWNING_ROOF = auto()
    PERGOLA_SIDE = auto()
    PERGOLA_SLAT_ROOF = auto()
    DIMMABLE_LIGHT = auto()
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
            self.VENEER,
            self.PERGOLA_AWNING_ROOF,
            self.PERGOLA_SIDE,
            self.PERGOLA_SLAT_ROOF,
        ]

    def is_light(self) -> bool:
        """Check if the type corresponds to any kind of light."""
        return self in [
            self.BASIC_LIGHT,
            self.DIMMABLE_LIGHT,
        ]

    @staticmethod
    def convert(lower: str):
        """Get the device type from the Onyx API's type information.

        lower: the lower case device type identifier"""
        try:
            return DeviceType[lower.upper()]
        except (KeyError, AttributeError):
            return None
