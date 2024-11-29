"""Tests for the SupportedVersions data class."""

from onyx_client.data.supported_versions import SupportedVersions
from onyx_client.utils.const import API_VERSION


class TestSupportedVersions:
    def test_supports(self):
        supported_versions = SupportedVersions([API_VERSION, "other"])
        assert supported_versions.supports(API_VERSION)
        assert supported_versions.supports("other")

    def test_supports_not(self):
        supported_versions = SupportedVersions(["other"])
        assert not supported_versions.supports(API_VERSION)
