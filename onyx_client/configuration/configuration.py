"""Onyx Client API configuration."""


class Configuration:
    """The API connection configuration."""

    def __init__(self, fingerprint: str, access_token: str):
        """Initialize the configuration.

        fingerprint: the ONYX.CENTER device fingerprint
        access_token: the access token to use"""
        self.fingerprint = fingerprint
        self.access_token = access_token
