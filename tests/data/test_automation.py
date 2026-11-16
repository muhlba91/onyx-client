"""Tests for the Automation data class."""

from onyx_client.data.automation import Automation


class TestAutomation:
    def test_create(self):
        assert Automation.create(
            {
                "id": "id",
                "name": "Wind protection",
                "emoji": "🌬",
                "type": "wind",
                "enabled": True,
            }
        ) == Automation("id", "Wind protection", "🌬", "wind", True)

    def test_create_minimal(self):
        assert Automation.create({"id": "http://o.hella.info/d/1"}) == Automation(
            "http://o.hella.info/d/1", None, None, None, False
        )

    def test_create_none(self):
        assert Automation.create(None) is None

    def test_str(self):
        assert (
            str(Automation("id", "Wind", None, "wind", True))
            == "Automation(id=id, name=Wind, type=wind, enabled=True)"
        )

    def test_not_eq(self):
        automation = Automation("id", "Wind", "🌬", "wind", True)
        assert automation != Automation("other", "Wind", "🌬", "wind", True)
        assert automation != Automation("id", "Rain", "🌬", "wind", True)
        assert automation != Automation("id", "Wind", None, "wind", True)
        assert automation != Automation("id", "Wind", "🌬", "sun", True)
        assert automation != Automation("id", "Wind", "🌬", "wind", False)
        assert automation != "id"
