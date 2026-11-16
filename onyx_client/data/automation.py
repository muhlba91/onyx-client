"""Automation of the ONYX.CENTER."""


class Automation:
    """A safety or comfort automation configured on the ONYX.CENTER."""

    def __init__(
        self,
        identifier: str,
        name: str | None,
        emoji: str | None,
        automation_type: str | None,
        enabled: bool,
    ):
        """Initialize the automation.

        identifier: the opaque automation identifier (a UUID or a URI)
        name: the display name
        emoji: the display emoji
        automation_type: the free-form type, e.g. wind
        enabled: set if the automation is active"""
        self.identifier = identifier
        self.name = name
        self.emoji = emoji
        self.automation_type = automation_type
        self.enabled = enabled

    def __str__(self) -> str:
        return f"Automation(id={self.identifier}, name={self.name}, type={self.automation_type}, enabled={self.enabled})"

    @staticmethod
    def create(properties: dict):
        """Create an automation from properties.

        properties: the properties of the automation"""
        if properties is None:
            return None

        return Automation(
            properties.get("id"),
            properties.get("name"),
            properties.get("emoji"),
            properties.get("type"),
            properties.get("enabled", False),
        )

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.identifier == other.identifier
                and self.name == other.name
                and self.emoji == other.emoji
                and self.automation_type == other.automation_type
                and self.enabled == other.enabled
            )
        return False
