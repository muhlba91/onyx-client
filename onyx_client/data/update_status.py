"""Software Update Status of the ONYX.CENTER."""


class UpdateStatus:
    """The installed and available software version of the ONYX.CENTER."""

    def __init__(
        self,
        current: str | None,
        available_version: str | None = None,
        progress: float | None = None,
    ):
        """Initialize the update status.

        current: the installed software version
        available_version: the version of the available update, if any
        progress: the transferred fraction (0-1) of the update, if transferring"""
        self.current = current
        self.available_version = available_version
        self.progress = progress

    def __str__(self) -> str:
        return f"UpdateStatus(current={self.current}, available_version={self.available_version}, progress={self.progress})"

    @staticmethod
    def create(properties: dict):
        """Create an update status from properties.

        properties: the properties of the update status"""
        if properties is None:
            return None

        available = properties.get("available") or {}
        return UpdateStatus(
            properties.get("current"),
            available.get("version"),
            available.get("progress"),
        )

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.current == other.current
                and self.available_version == other.available_version
                and self.progress == other.progress
            )
        return False
