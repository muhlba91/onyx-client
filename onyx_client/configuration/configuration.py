"""Onyx Client API configuration."""


class Configuration:
    """The API connection configuration."""

    def __init__(self, fingerprint: str, access_token: str):
        """Initialize the configuration."""
        self.fingerprint = fingerprint
        self.access_token = access_token
