"""Tests for the DeviceCommand data class."""
import pytest

from onyx_client.data.device_command import DeviceCommand
from onyx_client.enum.action import Action
from onyx_client.exception.invalid_command import InvalidCommandException


class TestDeviceCommand:
    def test_data_action(self):
        command = DeviceCommand(action=Action.STOP)
        assert command.data() == {"action": "stop"}

    def test_data_properties(self):
        command = DeviceCommand(properties={"property": 10})
        assert command.data() == {"properties": {"property": 10}}

    def test_data_action_and_properties(self):
        with pytest.raises(InvalidCommandException):
            DeviceCommand(action=Action.STOP, properties={"property": 10})

    def test_data_no_action_and_properties(self):
        with pytest.raises(InvalidCommandException):
            DeviceCommand()

    def test_data_valid_from(self):
        command = DeviceCommand(action=Action.STOP, valid_from=10)
        assert command.data() == {"action": "stop", "valid_from": 10}

    def test_data_best_before(self):
        command = DeviceCommand(action=Action.STOP, best_before=10)
        assert command.data() == {"action": "stop", "best_before": 10}
