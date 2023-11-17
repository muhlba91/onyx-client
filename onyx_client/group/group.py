"""Group class."""


class Group:
    """A ONYX controlled group."""

    def __init__(
        self,
        identifier: str,
        name: str,
        devices: list,
    ):
        """Initialize the group.

        identifier: the group identifier
        name: the group name
        devices: the list of devices belonging to the group"""
        self.identifier = identifier
        self.name = name
        self.devices = devices

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.identifier == other.identifier
        return False
