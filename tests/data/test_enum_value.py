"""Tests for the EnumValue data class."""

from onyx_client.data.enum_value import EnumValue


class TestEnumValue:
    def test_create(self):
        assert EnumValue.create(
            {
                "type": "enumeration",
                "value": "ok",
                "values": ["collision", "ok"],
                "readonly": True,
            }
        ) == EnumValue("ok", ["collision", "ok"], True)

    def test_create_value_only(self):
        assert EnumValue.create({"value": "ok"}) == EnumValue("ok", [], False)

    def test_create_none(self):
        assert EnumValue.create(None) is None

    def test_str(self):
        assert str(EnumValue("ok", [], True)) == "EnumValue(value=ok)"

    def test_as_bool(self):
        assert EnumValue("true", ["true", "false"], True).as_bool() is True
        assert EnumValue("false", ["true", "false"], True).as_bool() is False
        assert EnumValue(None, ["true", "false"], True).as_bool() is None

    def test_not_eq(self):
        value = EnumValue("ok", ["ok"], True)
        assert value != EnumValue("collision", ["ok"], True)
        assert value != EnumValue("ok", [], True)
        assert value != EnumValue("ok", ["ok"], False)
        assert value != "ok"
