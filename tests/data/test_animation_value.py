"""Tests for the AnimationValue data class."""
from onyx_client.data.animation_keyframe import AnimationKeyframe
from onyx_client.data.animation_value import AnimationValue


class TestAnimationValue:
    def test_create(self):
        expected = AnimationValue(
            1637499108.0069883, 90, [AnimationKeyframe("linear", 0, 0.791666666, 33)]
        )
        assert (
            AnimationValue.create(
                {
                    "start": 1637499108.0069883,
                    "current_value": 90,
                    "keyframes": [
                        {
                            "interpolation": "linear",
                            "delay": 0,
                            "duration": 0.791666666,
                            "value": 33,
                        }
                    ],
                }
            )
            == expected
        )

    def test_not_eq(self):
        assert AnimationValue(10, 10, list()) != 10
