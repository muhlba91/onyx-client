"""Date Information (date, time, timezone, ...) class."""


class DateInformation:
    """Container for all date related information of the ONYX.CENTER."""

    def __init__(self, time: float, timezone: str, timezone_offset: int):
        """Initialize the date information.

        time: the value
        timezone: the timezone of the device
        timezone_offset: the offset of the timezone"""
        self.time = time
        self.timezone = timezone
        self.timezone_offset = timezone_offset
