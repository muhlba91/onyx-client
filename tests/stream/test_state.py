"""Tests for the event stream state store."""

import json

import pytest

from onyx_client.device.shutter import Shutter
from onyx_client.stream.events import (
    AutomationsChanged,
    DeviceAdded,
    DeviceChanged,
    DeviceRemoved,
    GroupsChanged,
    Snapshot,
    UpdateChanged,
)
from onyx_client.stream.sse import parse
from onyx_client.stream.state import State

DEVICE = {"name": "Shutter", "type": "rollershutter"}


def snapshot(**kwargs) -> dict:
    return {
        "devices": {"d1": DEVICE},
        "groups": {"g1": {"name": "Group", "devices": ["d1"]}},
        "automations": [{"id": "a1", "enabled": True}],
        "update": {"current": "2.13.4"},
        **kwargs,
    }


async def replay(state: State, log: str) -> list:
    async def lines():
        for line in log.splitlines():
            yield line

    events = []
    async for event, data in parse(lines()):
        if event == "snapshot":
            events.extend(state.replace(json.loads(data)))
        elif event == "patch":
            events.extend(state.apply(json.loads(data)))
    return events


class TestState:
    def test_replace(self):
        events = State().replace(snapshot())
        assert len(events) == 1
        event = events[0]
        assert isinstance(event, Snapshot)
        assert isinstance(event.devices["d1"], Shutter)
        assert event.devices["d1"].identifier == "d1"
        assert event.groups["g1"].identifier == "g1"
        assert event.groups["g1"].devices == ["d1"]
        assert event.automations[0].identifier == "a1"
        assert event.update.current == "2.13.4"

    def test_replace_empty(self):
        event = State().replace({})[0]
        assert event.devices == {}
        assert event.groups == {}
        assert event.automations == []
        assert event.update is None

    def test_replace_removes_nulls(self):
        state = State()
        state.replace({"devices": {"d1": DEVICE, "d2": None}})
        assert state.data == {"devices": {"d1": DEVICE}}

    def test_replace_diffs_previous_state(self):
        state = State()
        state.replace(snapshot())
        events = state.replace(
            snapshot(
                devices={"d1": {**DEVICE, "name": "Renamed"}, "d2": DEVICE},
                groups={},
                automations=[],
                update={"current": "2.14.0"},
            )
        )
        assert [type(event) for event in events] == [
            Snapshot,
            DeviceChanged,
            DeviceAdded,
            GroupsChanged,
            AutomationsChanged,
            UpdateChanged,
        ]
        assert events[1].device.name == "Renamed"
        assert events[2].device.identifier == "d2"
        assert events[3].groups == {}
        assert events[4].automations == []
        assert events[5].update.current == "2.14.0"

    def test_replace_without_changes(self):
        state = State()
        state.replace(snapshot())
        assert [type(event) for event in state.replace(snapshot())] == [Snapshot]

    def test_apply_device_changed(self):
        state = State()
        state.replace(snapshot())
        events = state.apply({"devices": {"d1": {"tint": "#FFFFFF"}}})
        assert len(events) == 1
        assert isinstance(events[0], DeviceChanged)
        assert events[0].device.name == "Shutter"
        assert events[0].device.tint == "#FFFFFF"

    def test_apply_device_added_and_removed(self):
        state = State()
        state.replace(snapshot())
        events = state.apply({"devices": {"d1": None, "d2": DEVICE}})
        assert [type(event) for event in events] == [DeviceAdded, DeviceRemoved]
        assert events[0].device.identifier == "d2"
        assert events[1].identifier == "d1"

    def test_apply_unchanged(self):
        state = State()
        state.replace(snapshot())
        assert state.apply({"devices": {"d1": {"name": "Shutter"}}}) == []

    def test_apply_groups_automations_update(self):
        state = State()
        state.replace(snapshot())
        events = state.apply(
            {
                "groups": {"g1": None},
                "automations": [{"id": "a1", "enabled": False}],
                "update": {"available": {"version": "2.14.0", "progress": 0.5}},
            }
        )
        assert [type(event) for event in events] == [
            GroupsChanged,
            AutomationsChanged,
            UpdateChanged,
        ]
        assert events[0].groups == {}
        assert not events[1].automations[0].enabled
        assert events[2].update.available_version == "2.14.0"
        assert events[2].update.progress == 0.5

    def test_apply_before_snapshot(self):
        with pytest.raises(ValueError):
            State().apply({"devices": {}})

    @pytest.mark.asyncio
    async def test_captured_moves(self, captured):
        state = State()
        events = await replay(state, captured("events-v6.log"))
        assert isinstance(events[0], Snapshot)
        assert len(events[0].devices) == 8
        assert all(isinstance(event, DeviceChanged) for event in events[1:])
        assert len(events) > 40

    @pytest.mark.asyncio
    async def test_captured_natural_end(self, captured):
        state = State()
        events = await replay(state, captured("events-natural.log"))
        device = events[-1].device
        assert device.identifier == "00000000-0000-4000-8000-000000000008"
        # no patch after the natural end: stale value plus the finished animation
        position = device.actual_position
        assert position.value == 52
        assert position.is_animating(1794762018.5)
        assert not position.is_animating(1794762079)
        assert position.effective_value(1794762079) == 0
        # the active command outlives the movement
        assert device.active_command.best_before > 1794762079

    def test_invalid_data_keeps_state(self):
        state = State()
        state.replace(snapshot())
        with pytest.raises(AttributeError):
            state.apply({"devices": {"d1": "broken"}})
        with pytest.raises(AttributeError):
            state.replace({"devices": {"d1": "broken"}})
        assert state.data == snapshot()
