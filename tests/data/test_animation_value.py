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

    def test_create_no_keyframe(self):
        expected = AnimationValue(1637499108.0069883, 90, [])
        assert (
            AnimationValue.create(
                {
                    "start": 1637499108.0069883,
                    "current_value": 90,
                }
            )
            == expected
        )

    def test_create_no_data(self):
        expected = AnimationValue(None, None, [])
        assert AnimationValue.create({}) == expected

    def test_create_none(self):
        assert AnimationValue.create(None) is None

    def test_str(self):
        assert (
            str(
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
            )
            == "AnimationValue(start=1637499108.0069883, current_value=90, #keyframes=1)"
        )

    def test_not_eq(self):
        assert AnimationValue(10, 10, list()) != 10

    def test_update_with(self):
        value1 = AnimationValue(1.0, 1, [AnimationKeyframe("linear", 0, 1.0, 1)])
        value2 = AnimationValue(
            2.0,
            2,
            [
                AnimationKeyframe("linear", 1, 2.0, 2),
                AnimationKeyframe("linear", 2, 3.0, 3),
            ],
        )
        value1.update_with(value2)
        assert value1.start == 2.0
        assert value1.current_value == 2
        assert len(value1.keyframes) == 2
        assert value1.keyframes[0].delay == 1
        assert value1.keyframes[0].duration == 2.0
        assert value1.keyframes[0].value == 2

    def test_update_with_none(self):
        value1 = AnimationValue(1.0, 1, [AnimationKeyframe("linear", 0, 1.0, 1)])
        value2 = None
        value1.update_with(value2)
        assert value1.start == 1.0
        assert value1.current_value == 1
        assert len(value1.keyframes) == 1
        assert value1.keyframes[0].delay == 0
        assert value1.keyframes[0].duration == 1.0
        assert value1.keyframes[0].value == 1

    def test_update_with_partials(self):
        value1 = AnimationValue(1.0, 1, [AnimationKeyframe("linear", 0, 1.0, 1)])
        value2 = AnimationValue(
            None,
            2,
            [
                AnimationKeyframe("linear", 1, 2.0, 2),
                AnimationKeyframe("linear", 2, 3.0, 3),
            ],
        )
        value1.update_with(value2)
        assert value1.start == 1.0
        assert value1.current_value == 2
        assert len(value1.keyframes) == 2
        assert value1.keyframes[0].delay == 1
        assert value1.keyframes[0].duration == 2.0
        assert value1.keyframes[0].value == 2

        value1 = AnimationValue(1.0, 1, [AnimationKeyframe("linear", 0, 1.0, 1)])
        value2 = AnimationValue(
            2.0,
            None,
            [
                AnimationKeyframe("linear", 1, 2.0, 2),
                AnimationKeyframe("linear", 2, 3.0, 3),
            ],
        )
        value1.update_with(value2)
        assert value1.start == 2.0
        assert value1.current_value == 1
        assert len(value1.keyframes) == 2
        assert value1.keyframes[0].delay == 1
        assert value1.keyframes[0].duration == 2.0
        assert value1.keyframes[0].value == 2

        value1 = AnimationValue(1.0, 1, [AnimationKeyframe("linear", 0, 1.0, 1)])
        value2 = AnimationValue(2.0, 2, None)
        value1.update_with(value2)
        assert value1.start == 2.0
        assert value1.current_value == 2
        assert len(value1.keyframes) == 1
        assert value1.keyframes[0].delay == 0
        assert value1.keyframes[0].duration == 1.0
        assert value1.keyframes[0].value == 1
