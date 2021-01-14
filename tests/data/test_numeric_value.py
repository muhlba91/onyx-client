"""Tests for the NumericValue data class."""
from onyx_client.data.numeric_value import NumericValue


class TestNumericValue:
    def test_create(self):
        expected = NumericValue(10, 10, 100, True)
        assert (
            NumericValue.create(
                {"value": 10, "minimum": 10, "maximum": 100, "read_only": True}
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

    def test_not_eq(self):
        assert NumericValue(10, 10, 100, True) != 10
