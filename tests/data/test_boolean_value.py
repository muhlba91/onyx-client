"""Tests for the BooleanValue data class."""
from onyx_client.data.boolean_value import BooleanValue


class TestBooleanValue:
    def test_create(self):
        expected = BooleanValue(True, True)
        assert BooleanValue.create({"value": True, "read_only": True}) == expected

    def test_create_value_only(self):
        expected = BooleanValue(False, False)
        assert (
            BooleanValue.create(
                {
                    "value": False,
                }
            )
            == expected
        )

    def test_not_eq(self):
        assert BooleanValue(True, True) != 10
