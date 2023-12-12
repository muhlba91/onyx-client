"""Boolean Values of Onyx devices."""


class BooleanValue:
    """The representation of a boolean value."""

    def __init__(self, value: bool, read_only: bool):
        """Initialize the boolean value.

        value: the value
        read_only: set if the value is read only"""
        self.value = value
        self.read_only = read_only

    @staticmethod
    def create(properties: dict):
        """Create a boolean value from properties.

        properties: the properties of the device"""
        if properties is None:
            return None

        return BooleanValue(
            properties.get("value", "false") == "true",
            properties.get("read_only", "false") == "true",
        )

    def __str__(self) -> str:
        return f"BooleanValue(value={self.value})"

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.value == other.value and self.read_only == other.read_only
        return False
