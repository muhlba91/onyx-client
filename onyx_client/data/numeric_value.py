"""Numeric Values of Onyx devices."""

from ..data.animation_value import AnimationValue


class NumericValue:
    """The representation of a numeric value."""

    def __init__(
        self,
        value: int,
        minimum: int,
        maximum: int,
        readonly: bool,
        animation: AnimationValue | None = None,
    ):
        """Initialize the numeric value.

        value: the value
        minimum: the minimum supported value
        maximum: the maximum supported value
        readonly: set if the value is read only
        animation: an optional animation"""
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        self.readonly = readonly
        self.animation = animation

    def __str__(self) -> str:
        return f"NumericValue(value={self.value}, minimum={self.minimum}, maximum={self.maximum}, animation={self.animation})"

    @staticmethod
    def create(properties: dict):
        """Create a numeric value from properties.

        properties: the properties of the value"""
        if properties is None:
            return None

        return NumericValue(
            properties.get("value"),
            properties.get("minimum"),
            properties.get("maximum"),
            properties.get("readonly", False),
            AnimationValue.create(properties.get("animation")),
        )

    def effective_value(self, time: float) -> float | None:
        """Get the value at the provided time, taking the animation into account.

        ONYX keeps reporting the value from before an animation, even after the
        animation finished, so the animation takes precedence over the value.

        time: the UNIX timestamp (in ONYX.CENTER time)"""
        if self.animation is None or not self.animation.keyframes:
            return self.value
        return self.animation.value_at(time)

    def is_animating(self, time: float) -> bool:
        """Check if an animation is pending or running at the provided time.

        time: the UNIX timestamp (in ONYX.CENTER time)"""
        return (
            self.animation is not None
            and len(self.animation.keyframes) > 0
            and time < self.animation.end_time()
        )

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.value == other.value
                and self.minimum == other.minimum
                and self.maximum == other.maximum
                and self.readonly == other.readonly
                and self.animation == other.animation
            )
        return False
