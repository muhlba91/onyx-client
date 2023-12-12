"""Tests for the NumericValue data class."""
from onyx_client.data.animation_keyframe import AnimationKeyframe
from onyx_client.data.animation_value import AnimationValue
from onyx_client.data.numeric_value import NumericValue


class TestNumericValue:
    def test_create(self):
        expected = NumericValue(
            10,
            10,
            100,
            True,
            AnimationValue(10, 10, [AnimationKeyframe("linear", 10, 10, 10)]),
        )
        assert (
            NumericValue.create(
                {
                    "value": 10,
                    "minimum": 10,
                    "maximum": 100,
                    "read_only": True,
                    "animation": {
                        "start": 10,
                        "current_value": 10,
                        "keyframes": [
                            {
                                "interpolation": "linear",
                                "delay": 10,
                                "duration": 10,
                                "value": 10,
                            }
                        ],
                    },
                }
            )
            == expected
        )

    def test_create_value_only(self):
        expected = NumericValue(10, 0, 100, False)
        assert (
            NumericValue.create(
                {
                    "value": 10,
                }
            )
            == expected
        )

    def test_create_no_value(self):
        expected = NumericValue(None, 0, 100, False)
        assert NumericValue.create({}) == expected

    def test_create_none(self):
        assert NumericValue.create(None) is None

    def test_str(self):
        assert (
            str(
                NumericValue.create(
                    {
                        "value": 10,
                        "minimum": 10,
                        "maximum": 100,
                        "read_only": True,
                        "animation": {
                            "start": 10,
                            "current_value": 10,
                            "keyframes": [
                                {
                                    "interpolation": "linear",
                                    "delay": 10,
                                    "duration": 10,
                                    "value": 10,
                                }
                            ],
                        },
                    }
                )
            )
            == "NumericValue(value=10, minimum=10, maximum=100, animation=AnimationValue(start=10, current_value=10, #keyframes=1))"
        )

    def test_update_with(self):
        value = NumericValue(
            1,
            1,
            10,
            False,
            AnimationValue(1, 1, [AnimationKeyframe("linear", 1, 1, 1)]),
        )
        expected = NumericValue(
            10,
            10,
            100,
            True,
            AnimationValue(10, 10, [AnimationKeyframe("linear", 10, 10, 10)]),
        )
        value.update_with(expected)
        assert value == expected

    def test_update_with_only_existing(self):
        value = NumericValue(
            10,
            10,
            100,
            True,
        )
        expected = NumericValue(
            10,
            10,
            100,
            True,
            AnimationValue(10, 10, [AnimationKeyframe("linear", 10, 10, 10)]),
        )
        value.update_with(
            NumericValue(
                None,
                None,
                None,
                None,
                AnimationValue(10, 10, [AnimationKeyframe("linear", 10, 10, 10)]),
            )
        )
        assert value == expected

    def test_not_eq(self):
        assert NumericValue(10, 10, 100, True) != 10
