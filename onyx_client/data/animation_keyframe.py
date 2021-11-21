"""Animation Keyframe of Onyx devices."""


class AnimationKeyframe:
    """The representation of an animation keyframe."""

    def __init__(self, interpolation: str, delay: int, duration: float, value: int):
        """Initialize the animation keyframe."""
        self.interpolation = interpolation
        self.delay = delay
        self.duration = duration
        self.value = value

    @staticmethod
    def create(properties: dict):
        """Create an animation keyframe from properties."""
        return AnimationKeyframe(
            properties["interpolation"],
            properties["delay"],
            properties["duration"],
            properties["value"],
        )

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.interpolation == other.interpolation
                and self.delay == other.delay
                and self.duration == other.duration
                and self.value == other.value
            )
        return False
