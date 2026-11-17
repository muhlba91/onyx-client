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

    def test_repr_masks_token(self):
        config = Configuration("finger", "s3cr3t", local_address="1.2.3.4")
        assert "s3cr3t" not in repr(config)
        assert "s3cr3t" not in str(config)
        assert repr(config) == (
            "Configuration(fingerprint='finger', access_token='***', "
            "local_address='1.2.3.4', api_version='v6')"
        )

    def test_repr_without_token(self):
        assert "access_token=None" in repr(Configuration("finger", None))
