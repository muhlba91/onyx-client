"""Onyx Client API configuration."""

from ..exception.invalid_configuration import InvalidConfigurationException
from ..utils.const import API_VERSION, DEPRECATED_API_VERSION
from ..utils.sanitize import MASK


class Configuration:
    """The API connection configuration. Its repr masks the access token."""

    def __init__(
        self,
        fingerprint: str,
        access_token: str,
        local_address: str | None = None,
        api_version: str = API_VERSION,
    ):
        """Initialize the configuration.

        fingerprint: the ONYX.CENTER device fingerprint
        access_token: the access token to use
        local_address: the local address to use (default: None)
        api_version: the API version to use (default: v6, deprecated: v3)"""
        if api_version not in (API_VERSION, DEPRECATED_API_VERSION):
            raise InvalidConfigurationException("UNSUPPORTED_API_VERSION")

        self.fingerprint = fingerprint
        self.access_token = access_token
        self.local_address = local_address
        self.api_version = api_version

    @property
    def identifier(self) -> str:
        """Get the  identifier for this configuration."""
        return self.local_address if self.is_local else self.fingerprint

    @property
    def is_local(self) -> bool:
        """Return True if the configuration is set to use a local address."""
        return self.local_address is not None

    def __repr__(self) -> str:
        """Describe the configuration without the access token."""
        token = MASK if self.access_token else None
        return (
            f"Configuration(fingerprint={self.fingerprint!r}, "
            f"access_token={token!r}, local_address={self.local_address!r}, "
            f"api_version={self.api_version!r})"
        )
