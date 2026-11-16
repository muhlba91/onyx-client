"""Verification results of the ONYX.CENTER connection."""

from enum import Enum, auto


class VerifyResult(Enum):
    """The result of verifying the connection to the ONYX.CENTER."""

    OK = auto()
    UNREACHABLE = auto()
    UNAUTHORIZED = auto()
    VERSION_UNSUPPORTED = auto()
