"""Events emitted by the Onyx event stream."""

from ..data.update_status import UpdateStatus
from ..device.device import Device


class Event:
    """Base class of all stream events."""


class Snapshot(Event):
    """The complete state after every (re)connect."""

    def __init__(
        self,
        devices: dict,
        groups: dict,
        automations: list,
        update: UpdateStatus | None,
    ):
        """Initialize the event.

        devices: the devices by identifier
        groups: the groups by identifier
        automations: the automations in app order
        update: the update status, if known"""
        self.devices = devices
        self.groups = groups
        self.automations = automations
        self.update = update


class DeviceAdded(Event):
    """A device was added."""

    def __init__(self, device: Device):
        """Initialize the event.

        device: the complete device"""
        self.device = device


class DeviceChanged(Event):
    """A device changed."""

    def __init__(self, device: Device):
        """Initialize the event.

        device: the complete device"""
        self.device = device


class DeviceRemoved(Event):
    """A device was removed."""

    def __init__(self, identifier: str):
        """Initialize the event.

        identifier: the identifier of the removed device"""
        self.identifier = identifier


class GroupsChanged(Event):
    """Any group was added, changed or removed."""

    def __init__(self, groups: dict):
        """Initialize the event.

        groups: all groups by identifier"""
        self.groups = groups


class AutomationsChanged(Event):
    """Any automation was added, changed, removed or reordered."""

    def __init__(self, automations: list):
        """Initialize the event.

        automations: all automations in app order"""
        self.automations = automations


class UpdateChanged(Event):
    """The update status changed."""

    def __init__(self, update: UpdateStatus | None):
        """Initialize the event.

        update: the update status, if known"""
        self.update = update


class Pulse(Event):
    """The periodic heartbeat of the ONYX.CENTER."""

    def __init__(self, time: float):
        """Initialize the event.

        time: the ONYX.CENTER time as UNIX timestamp"""
        self.time = time


class Resynced(Event):
    """The stream reconnected; the following snapshot replaces the state."""

    def __init__(self, reason: str):
        """Initialize the event.

        reason: why the stream reconnected"""
        self.reason = reason
