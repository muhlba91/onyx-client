"""Tests for the Configuration class."""

import pytest

from onyx_client.configuration.configuration import Configuration
from onyx_client.exception.invalid_configuration import InvalidConfigurationException


class TestConfiguration:
    def test_init(self):
        config = Configuration("finger", "token")
        assert config.fingerprint == "finger"
        assert config.access_token == "token"
        assert config.local_address is None
        assert config.api_version == "v6"

    def test_init_deprecated_api_version(self):
        config = Configuration("finger", "token", api_version="v3")
        assert config.api_version == "v3"

    def test_init_unsupported_api_version(self):
        with pytest.raises(InvalidConfigurationException):
            Configuration("finger", "token", api_version="v5")

    def test_init_local_address(self):
        config = Configuration("finger", "token", local_address="localhost")
        assert config.fingerprint == "finger"
        assert config.access_token == "token"
        assert config.local_address == "localhost"

    def test_identifier_fingerprint(self):
        config = Configuration("finger", "token")
        assert config.identifier == "finger"

    def test_identifier_local_address(self):
        config = Configuration("finger", "token", local_address="localhost")
        assert config.identifier == "localhost"

    def test_is_not_local(self):
        config = Configuration("finger", "token")
        assert not config.is_local

    def test_is_local(self):
        config = Configuration("finger", "token", local_address="localhost")
        assert config.is_local
