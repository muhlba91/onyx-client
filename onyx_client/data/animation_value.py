"""Animation Values of Onyx devices."""

from ..data.animation_keyframe import AnimationKeyframe


class AnimationValue:
    """The representation of an animation value.

    Keyframes run one after another: each waits for its delay, then changes the
    value linearly to its own value within its duration (instantly if the
    duration is not positive; negative delays count as 0). A keyframe without
    a value keeps the previous value. Unknown interpolations fall back to
    linear."""

    def __init__(self, start: float, current_value: int, keyframes: list):
        """Initialize the animation value.

        start: the start time as UNIX timestamp
        current_value: the value at the start of the animation
        keyframes: the list of keyframes until the end of the animation"""
        self.start = start
        self.current_value = current_value
        self.keyframes = keyframes

    def __str__(self) -> str:
        return f"AnimationValue(start={self.start}, current_value={self.current_value}, #keyframes={len(self.keyframes)})"

    @staticmethod
    def create(properties: dict):
        """Create an animation value from properties.

        properties: the properties of the animation"""
        if properties is None:
            return None

        return AnimationValue(
            properties.get("start") or 0,
            properties.get("current_value") or 0,
            [
                AnimationKeyframe.create(keyframe)
                for keyframe in properties.get("keyframes") or []
                if keyframe is not None
            ],
        )

    def end_time(self) -> float:
        """Get the end time of the animation as UNIX timestamp."""
        return self.start + sum(
            max(keyframe.delay, 0) + max(keyframe.duration, 0)
            for keyframe in self.keyframes
        )

    def value_at(self, time: float) -> float:
        """Get the value of the animation at the provided time.

        time: the UNIX timestamp (in ONYX.CENTER time)"""
        value = self.current_value
        segment_start = self.start
        for keyframe in self.keyframes:
            target = value if keyframe.value is None else keyframe.value
            segment_start += max(keyframe.delay, 0)
            if time < segment_start:
                return value
            if keyframe.duration > 0:
                if time < segment_start + keyframe.duration:
                    progress = (time - segment_start) / keyframe.duration
                    return value + (target - value) * progress
                segment_start += keyframe.duration
            value = target
        return value

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.start == other.start
                and self.current_value == other.current_value
                and self.keyframes == other.keyframes
            )
        return False
