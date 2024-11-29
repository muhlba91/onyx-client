"""Numeric Values of Onyx devices."""

from typing import Optional

from ..data.animation_value import AnimationValue


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
        """Initialize the numeric value.

        value: the value
        minimum: the minimum supported value
        maximum: the maximum supported value
        read_only: set of the value is read only
        animation: an optional ongoing animation"""
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        self.read_only = read_only
        self.animation = animation

    def __str__(self) -> str:
        return f"NumericValue(value={self.value}, minimum={self.minimum}, maximum={self.maximum}, animation={self.animation})"

    @staticmethod
    def create(properties: dict):
        """Create a numeric value from properties.

        properties: the properties of the device"""
        if properties is None:
            return None

        return NumericValue(
            properties.get("value", None),
            properties.get("minimum", None),
            properties.get("maximum", None),
            properties.get("read_only", False),
            AnimationValue.create(properties.get("animation", None)),
        )

    def update_with(self, other: Optional["NumericValue"]):
        """Updates this value with the target.

        other: the other value"""
        if other is not None:
            self.value = self.value if other.value is None else other.value
            self.minimum = self.minimum if other.minimum is None else other.minimum
            self.maximum = self.maximum if other.maximum is None else other.maximum
            self.read_only = (
                self.read_only if other.read_only is None else other.read_only
            )
            # if other.animation is None it would mean that the animation is cancelled by Onyx.
            # in fact, we can just overwrite it no matter the value.
            self.animation = other.animation

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
