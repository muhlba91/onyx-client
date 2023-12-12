"""Tests for the BooleanValue data class."""
from onyx_client.data.boolean_value import BooleanValue


class TestBooleanValue:
    def test_create(self):
        expected = BooleanValue(True, True)
        assert BooleanValue.create({"value": "true", "read_only": "true"}) == expected

    def test_create_string_boolean(self):
        expected = BooleanValue(False, False)
        assert BooleanValue.create({"value": "false", "read_only": "false"}) == expected

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

    def test_create_none(self):
        assert BooleanValue.create(None) is None

    def test_str(self):
        assert (
            str(
                BooleanValue.create(
                    {
                        "value": "true",
                    }
                )
            )
            == "BooleanValue(value=True)"
        )

    def test_not_eq(self):
        assert BooleanValue(True, True) != 10
