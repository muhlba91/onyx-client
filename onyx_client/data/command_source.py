"""Command Source of an active Onyx command."""


class CommandSource:
    """The source an active command was issued by."""

    def __init__(
        self,
        source_type: str | None,
        identifier: str | None,
        name: str | None,
        emoji: str | None,
    ):
        """Initialize the command source.

        source_type: the source type (client, automation, device)
        identifier: the automation or device identifier
        name: the display name
        emoji: the display emoji"""
        self.source_type = source_type
        self.identifier = identifier
        self.name = name
        self.emoji = emoji

    def __str__(self) -> str:
        return f"CommandSource(type={self.source_type}, id={self.identifier}, name={self.name})"

    @staticmethod
    def create(properties: dict):
        """Create a command source from properties.

        properties: the properties of the source"""
        if properties is None:
            return None

        return CommandSource(
            properties.get("type"),
            properties.get("id"),
            properties.get("name"),
            properties.get("emoji"),
        )

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.source_type == other.source_type
                and self.identifier == other.identifier
                and self.name == other.name
                and self.emoji == other.emoji
            )
        return False
