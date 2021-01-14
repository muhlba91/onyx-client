"""Date Information (date, time, timezone, ...) class."""


class DateInformation:
    """Container for all date related information of the ONYX.CENTER."""

    def __init__(self, time: float, timezone: str, timezone_offset: int):
        """Initialize the date information."""
        self.time = time
        self.timezone = timezone
        self.timezone_offset = timezone_offset
