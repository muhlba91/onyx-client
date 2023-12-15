"""Animation Values of Onyx devices."""
from typing import Optional

from ..data.animation_keyframe import AnimationKeyframe


class AnimationValue:
    """The representation of an animation value."""

    def __init__(self, start: float, current_value: int, keyframes: list):
        """Initialize the animation value.

        start: the start value
        current_value: the current value in the animation
        keyframes: the list of keyframes until the end of the animation"""
        self.start = start
        self.current_value = current_value
        self.keyframes = keyframes

    def __str__(self) -> str:
        return f"AnimationValue(start={self.start}, current_value={self.current_value}, #keyframes={len(self.keyframes)})"

    @staticmethod
    def create(properties: dict):
        """Create an animation value from properties.

        properties: the properties of the device"""
        if properties is None:
            return None

        return AnimationValue(
            properties.get("start", None),
            properties.get("current_value"),
            [
                AnimationKeyframe.create(keyframe)
                for keyframe in properties.get("keyframes", list())
            ],
        )

    def update_with(self, other: Optional["AnimationValue"]):
        """Updates this value with the target.

        other: the other value"""
        if other is not None:
            self.start = self.start if other.start is None else other.start
            self.current_value = (
                self.current_value
                if other.current_value is None
                else other.current_value
            )
            self.keyframes = (
                self.keyframes if other.keyframes is None else other.keyframes
            )

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.start == other.start and self.current_value == other.current_value
            )
        return False
