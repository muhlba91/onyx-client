"""Device Actions of Onyx devices."""
from enum import Enum, auto


class Action(Enum):
    """The actions supported by Onyx."""

    CLOSE = auto()
    OPEN = auto()
    STOP = auto()
    TILT_DOWN = auto()
    TILT_UP = auto()
    WINK = auto()
    LIGHT_ON = auto()
    LIGHT_OFF = auto()

    def string(self) -> str:
        """Get the string representation for the Onyx API."""
        return self.name.lower()

    @staticmethod
    def convert(lower: str):
        """Get the action from the Onyx API's type information."""
        try:
            return Action[lower.upper()]
        except KeyError:
            return None
