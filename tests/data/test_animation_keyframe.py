"""Tests for the AnimationKeyframe data class."""

from onyx_client.data.animation_keyframe import AnimationKeyframe


class TestAnimationKeyframe:
    def test_create(self):
        assert AnimationKeyframe.create(
            {"value": 10, "duration": 1.5, "delay": 0.5, "interpolation": "linear"}
        ) == AnimationKeyframe(10, 1.5, 0.5, "linear")

    def test_create_defaults(self):
        keyframe = AnimationKeyframe.create(
            {"value": 10, "duration": None, "delay": None, "interpolation": None}
        )
        assert keyframe == AnimationKeyframe(10)
        assert keyframe.duration == 0
        assert keyframe.delay == 0
        assert keyframe.interpolation == "linear"

    def test_create_keeps_interpolation(self):
        assert AnimationKeyframe.create({"interpolation": "cubic"}).interpolation == (
            "cubic"
        )

    def test_create_none(self):
        assert AnimationKeyframe.create(None) is None

    def test_str(self):
        assert (
            str(AnimationKeyframe(10, 1.5, 0.5, "linear"))
            == "AnimationKeyframe(value=10, duration=1.5, delay=0.5, interpolation=linear)"
        )

    def test_eq(self):
        assert AnimationKeyframe(10, 1, 0) == AnimationKeyframe(10, 1, 0, "linear")

    def test_not_eq(self):
        keyframe = AnimationKeyframe(10, 1, 0, "linear")
        assert keyframe != AnimationKeyframe(11, 1, 0, "linear")
        assert keyframe != AnimationKeyframe(10, 2, 0, "linear")
        assert keyframe != AnimationKeyframe(10, 1, 1, "linear")
        assert keyframe != AnimationKeyframe(10, 1, 0, "cubic")
        assert keyframe != 10
