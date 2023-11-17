"""Supported Versions class."""


class SupportedVersions:
    """Container for all supported versions by the ONYX.CENTER."""

    def __init__(self, versions: list):
        """Initialize the versions.

        versions: a list of supported versions"""
        self.versions = versions

    def supports(self, version: str) -> bool:
        """Check if the provided version is supported.

        version: the version to check for"""
        return version in self.versions
