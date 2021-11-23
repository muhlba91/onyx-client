"""Tests for the Configuration class."""
from onyx_client.configuration.configuration import Configuration


class TestConfiguration:
    def test_init(self):
        config = Configuration("finger", "token")
        assert config.fingerprint == "finger"
        assert config.access_token == "token"
