"""Tests for the AnimationKeyframe data class."""
from onyx_client.data.animation_keyframe import AnimationKeyframe


class TestAnimationKeyframe:
    def test_create(self):
        expected = AnimationKeyframe("linear", 0, 0.791666666, 33)
        assert (
            AnimationKeyframe.create(
                {
                    "interpolation": "linear",
                    "delay": 0,
                    "duration": 0.791666666,
                    "value": 33,
                }
            )
            == expected
        )

    def test_not_eq(self):
        assert AnimationKeyframe("linear", 0, 0, 0) != 10
