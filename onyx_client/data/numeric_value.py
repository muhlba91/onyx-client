"""Numeric Values of Onyx devices."""
from typing import Optional

from onyx_client.data.animation_value import AnimationValue


class NumericValue:
    """The representation of a numeric value."""

    def __init__(
        self,
        value: int,
        minimum: int,
        maximum: int,
        read_only: bool,
        animation: Optional[AnimationValue] = None,
    ):
        """Initialize the numeric value."""
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        self.read_only = read_only
        self.animation = animation

    @staticmethod
    def create(properties: dict):
        """Create a numeric value from properties."""
        if properties is None:
            return None

        return NumericValue(
            properties.get("value", None),
            properties.get("minimum", 0),
            properties.get("maximum", 100),
            properties.get("read_only", False),
            AnimationValue.create(properties.get("animation", None)),
        )

    def update_with(self, other: Optional):
        """Updates this value with the target."""
        if other is not None:
            self.value = self.value if other.value is None else other.value
            self.minimum = self.minimum if other.minimum is None else other.minimum
            self.maximum = self.maximum if other.maximum is None else other.maximum
            self.read_only = (
                self.read_only if other.read_only is None else other.read_only
            )
            self.animation = (
                self.animation if other.animation is None else other.animation
            )

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.value == other.value
                and self.minimum == other.minimum
                and self.maximum == other.maximum
                and self.read_only == other.read_only
                and self.animation == other.animation
            )
        return False
