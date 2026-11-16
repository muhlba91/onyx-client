"""State store of the Onyx event stream."""

from ..data.automation import Automation
from ..data.update_status import UpdateStatus
from ..utils.mapper import init_device, init_group
from ..utils.merge import merge_patch
from .events import (
    AutomationsChanged,
    DeviceAdded,
    DeviceChanged,
    DeviceRemoved,
    Event,
    GroupsChanged,
    Snapshot,
    UpdateChanged,
)


class State:
    """The raw JSON state of the event stream.

    A snapshot replaces the state, a patch is merged into it. Both return the
    events describing the differences to the previous state and leave the state
    unchanged if the data is invalid."""

    def __init__(self):
        """Initialize the empty state."""
        self.data = None

    def replace(self, snapshot: dict) -> list[Event]:
        """Replace the state with a snapshot.

        Returns the snapshot event, followed by the differences to the previous
        state if there was one.

        snapshot: the snapshot data"""
        data = merge_patch({}, snapshot)  # copy without nulls
        events = [
            Snapshot(
                {key: init_device(key, value) for key, value in _devices(data)},
                _groups(data),
                _automations(data),
                UpdateStatus.create(data.get("update")),
            )
        ]
        if self.data is not None:
            events.extend(_diff(self.data, data))
        self.data = data
        return events

    def apply(self, patch: dict) -> list[Event]:
        """Merge a patch into the state.

        Raises ValueError if no snapshot was received yet.

        patch: the JSON merge patch"""
        if self.data is None:
            raise ValueError("PATCH_BEFORE_SNAPSHOT")
        data = merge_patch(self.data, patch)
        events = _diff(self.data, data)
        self.data = data
        return events


def _diff(old: dict, new: dict) -> list[Event]:
    """Get the events describing the differences between two states.

    old: the previous state
    new: the current state"""
    old_devices, new_devices = dict(_devices(old)), dict(_devices(new))
    events = []
    for key, value in new_devices.items():
        if key not in old_devices:
            events.append(DeviceAdded(init_device(key, value)))
        elif old_devices[key] != value:
            events.append(DeviceChanged(init_device(key, value)))
    events.extend(DeviceRemoved(key) for key in old_devices if key not in new_devices)
    if old.get("groups") != new.get("groups"):
        events.append(GroupsChanged(_groups(new)))
    if old.get("automations") != new.get("automations"):
        events.append(AutomationsChanged(_automations(new)))
    if old.get("update") != new.get("update"):
        events.append(UpdateChanged(UpdateStatus.create(new.get("update"))))
    return events


def _devices(data: dict):
    """Get the (identifier, device data) pairs of a state.

    data: the state"""
    return (data.get("devices") or {}).items()


def _groups(data: dict) -> dict:
    """Get the groups of a state by identifier.

    data: the state"""
    return {
        key: init_group(key, value) for key, value in (data.get("groups") or {}).items()
    }


def _automations(data: dict) -> list:
    """Get the automations of a state.

    data: the state"""
    return [Automation.create(value) for value in data.get("automations") or []]
