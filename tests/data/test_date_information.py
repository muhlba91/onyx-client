"""Tests for the DateInformation data class."""
from onyx_client.data.date_information import DateInformation


class TestDateInformation:
    def test_init(self):
        date = DateInformation(10.9, "zone", 100)
        assert date.time == 10.9
        assert date.timezone == "zone"
        assert date.timezone_offset == 100
