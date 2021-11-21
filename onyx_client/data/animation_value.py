"""Animation Values of Onyx devices."""
from onyx_client.data.animation_keyframe import AnimationKeyframe


class AnimationValue:
    """The representation of an animation value."""

    def __init__(self, start: float, current_value: int, keyframes: list):
        """Initialize the animation value."""
        self.start = start
        self.current_value = current_value
        self.keyframes = keyframes

    @staticmethod
    def create(properties: dict):
        """Create an animation value from properties."""
        return AnimationValue(
            properties["start"],
            properties["current_value"],
            [
                AnimationKeyframe.create(keyframe)
                for keyframe in properties["keyframes"]
            ],
        )

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.start == other.start and self.current_value == other.current_value
            )
        return False
