"""Enumeration Values of Onyx devices."""


class EnumValue:
    """The representation of an enumeration value."""

    def __init__(self, value: str | None, values: list, readonly: bool):
        """Initialize the enumeration value.

        value: the value
        values: the list of valid values
        readonly: set if the value is read only"""
        self.value = value
        self.values = values
        self.readonly = readonly

    def __str__(self) -> str:
        return f"EnumValue(value={self.value})"

    @staticmethod
    def create(properties: dict):
        """Create an enumeration value from properties.

        properties: the properties of the value"""
        if properties is None:
            return None

        return EnumValue(
            properties.get("value"),
            properties.get("values") or [],
            properties.get("readonly", False),
        )

    def as_bool(self) -> bool | None:
        """Get the value of a "true"/"false" enumeration as boolean."""
        return None if self.value is None else self.value == "true"

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.value == other.value
                and self.values == other.values
                and self.readonly == other.readonly
            )
        return False
