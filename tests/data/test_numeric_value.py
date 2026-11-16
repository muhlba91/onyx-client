"""Tests for the NumericValue data class."""

from onyx_client.data.animation_keyframe import AnimationKeyframe
from onyx_client.data.animation_value import AnimationValue
from onyx_client.data.numeric_value import NumericValue


class TestNumericValue:
    def test_create(self):
        assert NumericValue.create(
            {
                "type": "numeric",
                "value": 10,
                "minimum": 0,
                "maximum": 100,
                "readonly": True,
                "animation": {
                    "start": 10,
                    "current_value": 10,
                    "keyframes": [{"value": 20, "duration": 1}],
                },
            }
        ) == NumericValue(
            10, 0, 100, True, AnimationValue(10, 10, [AnimationKeyframe(20, 1)])
        )

    def test_create_value_only(self):
        assert NumericValue.create({"value": 10}) == NumericValue(10, None, None, False)

    def test_create_none(self):
        assert NumericValue.create(None) is None

    def test_str(self):
        assert (
            str(NumericValue(10, 0, 100, True))
            == "NumericValue(value=10, minimum=0, maximum=100, animation=None)"
        )

    def test_eq(self):
        assert NumericValue(10, 0, 100, True) == NumericValue(10, 0, 100, True)

    def test_not_eq(self):
        value = NumericValue(10, 0, 100, True, AnimationValue(0, 0, []))
        assert value != NumericValue(11, 0, 100, True, AnimationValue(0, 0, []))
        assert value != NumericValue(10, 1, 100, True, AnimationValue(0, 0, []))
        assert value != NumericValue(10, 0, 99, True, AnimationValue(0, 0, []))
        assert value != NumericValue(10, 0, 100, False, AnimationValue(0, 0, []))
        assert value != NumericValue(10, 0, 100, True)
        assert value != 10

    def test_effective_value_without_animation(self):
        assert NumericValue(52, 0, 100, True).effective_value(100) == 52

    def test_effective_value_without_keyframes(self):
        value = NumericValue(52, 0, 100, True, AnimationValue(0, 0, []))
        assert value.effective_value(100) == 52

    def test_effective_value_animating(self):
        value = NumericValue(
            52, 0, 100, True, AnimationValue(100, 52, [AnimationKeyframe(100, 10)])
        )
        assert value.effective_value(105) == 76

    def test_effective_value_after_natural_end(self):
        # ONYX keeps the stale value and the finished animation (see fixtures)
        value = NumericValue(
            52, 0, 100, True, AnimationValue(100, 52, [AnimationKeyframe(100, 10)])
        )
        assert value.effective_value(300) == 100

    def test_is_animating(self):
        value = NumericValue(
            52, 0, 100, True, AnimationValue(100, 52, [AnimationKeyframe(100, 10)])
        )
        assert value.is_animating(99)
        assert value.is_animating(109.9)
        assert not value.is_animating(110)

    def test_is_animating_without_animation(self):
        assert not NumericValue(52, 0, 100, True).is_animating(0)
        assert not NumericValue(
            52, 0, 100, True, AnimationValue(100, 52, [])
        ).is_animating(0)
