"""Command Attributes of Onyx device commands."""

from enum import Enum, auto


class CommandAttribute(Enum):
    """The command attributes supported by Onyx."""

    URGENT = auto()
    FAST = auto()
    SLOW = auto()
    SILENT = auto()
    EFFICIENT = auto()

    def string(self) -> str:
        """Get the string representation for the Onyx API."""
        return self.name.lower()

    @staticmethod
    def convert(lower: str):
        """Get the command attribute from the Onyx API's attribute information.

        lower: the lower case attribute identifier"""
        try:
            return CommandAttribute[lower.upper()]
        except (KeyError, AttributeError):
            return None
