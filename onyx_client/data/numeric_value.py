"""Numeric Values of Onyx devices."""


class NumericValue:
    """The representation of a numeric value."""

    def __init__(self, value: int, minimum: int, maximum: int, read_only: bool):
        """Initialize the numeric value."""
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        self.read_only = read_only

    @staticmethod
    def create(properties: dict):
        """Create a numeric value from properties."""
        return NumericValue(
            properties["value"],
            properties.get("minimum", 0),
            properties.get("maximum", 100),
            properties.get("read_only", False),
        )

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.value == other.value
                and self.minimum == other.minimum
                and self.maximum == other.maximum
                and self.read_only == other.read_only
            )
        return False
