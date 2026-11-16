"""Animation Keyframe of Onyx devices."""


class AnimationKeyframe:
    """The representation of an animation keyframe."""

    def __init__(
        self,
        value: int | None,
        duration: float = 0,
        delay: float = 0,
        interpolation: str = "linear",
    ):
        """Initialize the animation keyframe.

        value: the value to interpolate to (None keeps the previous value)
        duration: the duration of the change in seconds
        delay: the delay before the change in seconds
        interpolation: the interpolation algorithm (only linear is supported)"""
        self.value = value
        self.duration = duration
        self.delay = delay
        self.interpolation = interpolation

    @staticmethod
    def create(properties: dict):
        """Create an animation keyframe from properties.

        properties: the properties of the keyframe"""
        if properties is None:
            return None

        return AnimationKeyframe(
            properties.get("value"),
            properties.get("duration") or 0,
            properties.get("delay") or 0,
            properties.get("interpolation") or "linear",
        )

    def __str__(self) -> str:
        return f"AnimationKeyframe(value={self.value}, duration={self.duration}, delay={self.delay}, interpolation={self.interpolation})"

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.value == other.value
                and self.duration == other.duration
                and self.delay == other.delay
                and self.interpolation == other.interpolation
            )
        return False
