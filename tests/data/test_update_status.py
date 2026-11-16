"""Tests for the UpdateStatus data class."""

from onyx_client.data.update_status import UpdateStatus


class TestUpdateStatus:
    def test_create(self):
        assert UpdateStatus.create(
            {"current": "2.13.0", "available": {"version": "2.14.0", "progress": 0.5}}
        ) == UpdateStatus("2.13.0", "2.14.0", 0.5)

    def test_create_up_to_date(self):
        assert UpdateStatus.create({"current": "2.13.4-0-geb8e366"}) == UpdateStatus(
            "2.13.4-0-geb8e366"
        )

    def test_create_none(self):
        assert UpdateStatus.create(None) is None

    def test_str(self):
        assert (
            str(UpdateStatus("2.13.0", "2.14.0"))
            == "UpdateStatus(current=2.13.0, available_version=2.14.0, progress=None)"
        )

    def test_not_eq(self):
        status = UpdateStatus("2.13.0", "2.14.0", 0.5)
        assert status != UpdateStatus("2.12.0", "2.14.0", 0.5)
        assert status != UpdateStatus("2.13.0", None, 0.5)
        assert status != UpdateStatus("2.13.0", "2.14.0", None)
        assert status != "2.13.0"
