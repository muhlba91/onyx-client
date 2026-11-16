"""Tests for the AnimationValue data class."""

import pytest

from onyx_client.data.animation_keyframe import AnimationKeyframe
from onyx_client.data.animation_value import AnimationValue


class TestAnimationValue:
    def test_create(self):
        assert AnimationValue.create(
            {
                "start": 1794761689.5,
                "current_value": 90,
                "keyframes": [
                    {
                        "value": 33,
                        "duration": 0.79,
                        "delay": 0.5,
                        "interpolation": "linear",
                    },
                    None,
                ],
            }
        ) == AnimationValue(1794761689.5, 90, [AnimationKeyframe(33, 0.79, 0.5)])

    def test_create_defaults(self):
        assert AnimationValue.create(
            {"start": None, "current_value": None, "keyframes": None}
        ) == AnimationValue(0, 0, [])

    def test_create_none(self):
        assert AnimationValue.create(None) is None

    def test_str(self):
        assert (
            str(AnimationValue(10, 20, [AnimationKeyframe(30)]))
            == "AnimationValue(start=10, current_value=20, #keyframes=1)"
        )

    def test_eq(self):
        assert AnimationValue(10, 20, [AnimationKeyframe(30)]) == AnimationValue(
            10, 20, [AnimationKeyframe(30)]
        )

    def test_not_eq(self):
        animation = AnimationValue(10, 20, [AnimationKeyframe(30)])
        assert animation != AnimationValue(11, 20, [AnimationKeyframe(30)])
        assert animation != AnimationValue(10, 21, [AnimationKeyframe(30)])
        assert animation != AnimationValue(10, 20, [AnimationKeyframe(31)])
        assert animation != 10

    def test_end_time(self):
        animation = AnimationValue(
            100,
            0,
            [AnimationKeyframe(50, 10, 0.5), AnimationKeyframe(80, -1, 1)],
        )
        assert animation.end_time() == 111.5

    def test_end_time_no_keyframes(self):
        assert AnimationValue(100, 0, []).end_time() == 100

    @pytest.mark.parametrize(
        ("time", "expected"),
        [
            (90, 0),
            (100, 0),
            (100.5, 0),
            (105.5, 25),
            (110.5, 50),
            (111, 50),
            (111.5, 80),
            (120, 80),
        ],
    )
    def test_value_at(self, time, expected):
        animation = AnimationValue(
            100,
            0,
            [AnimationKeyframe(50, 10, 0.5), AnimationKeyframe(80, 0, 1)],
        )
        assert animation.value_at(time) == expected

    @pytest.mark.parametrize(("time", "expected"), [(0, 100), (5, 50), (10, 0)])
    def test_value_at_decreasing(self, time, expected):
        assert AnimationValue(0, 100, [AnimationKeyframe(0, 10)]).value_at(
            time
        ) == pytest.approx(expected)

    def test_value_at_keyframe_without_value(self):
        animation = AnimationValue(
            0, 10, [AnimationKeyframe(None, 5), AnimationKeyframe(20, 5)]
        )
        assert animation.value_at(5) == 10
        assert animation.value_at(7.5) == 15

    def test_value_at_no_keyframes(self):
        assert AnimationValue(0, 10, []).value_at(100) == 10

    def test_value_at_negative_duration(self):
        animation = AnimationValue(0, 11, [AnimationKeyframe(100, -1)])
        assert animation.value_at(-1) == 11
        assert animation.value_at(0) == 100

    def test_negative_delay(self):
        animation = AnimationValue(0, 0, [AnimationKeyframe(10, 10, -5)])
        assert animation.end_time() == 10
        assert animation.value_at(5) == 5

    def test_value_at_short_duration(self):
        animation = AnimationValue(0, 0, [AnimationKeyframe(10, 0.5)])
        assert animation.value_at(0.25) == 5
