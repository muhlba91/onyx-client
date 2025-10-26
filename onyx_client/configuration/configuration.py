"""Onyx Client API configuration."""


class Configuration:
    """The API connection configuration."""

    def __init__(self, fingerprint: str, access_token: str, local_address: str = None):
        """Initialize the configuration.

        fingerprint: the ONYX.CENTER device fingerprint
        access_token: the access token to use
        local_address: the local address to use (default: None)"""
        self.fingerprint = fingerprint
        self.access_token = access_token
        self.local_address = local_address

    @property
    def identifier(self) -> str:
        """Get the  identifier for this configuration."""
        return self.local_address if self.is_local else self.fingerprint

    @property
    def is_local(self) -> bool:
        """Return True if the configuration is set to use a local address."""
        return self.local_address is not None
