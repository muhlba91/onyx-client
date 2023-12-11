"""Onyx Client API class."""
import json
import logging
from typing import Optional
from random import uniform

import aiohttp
import asyncio

from onyx_client.configuration.configuration import Configuration
from onyx_client.data.date_information import DateInformation
from onyx_client.data.device_command import DeviceCommand
from onyx_client.data.supported_versions import SupportedVersions
from onyx_client.device.device import Device
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType
from onyx_client.group.group import Group
from onyx_client.helpers.url import UrlHelper
from onyx_client.utils.const import API_VERSION
from onyx_client.utils.filter import present
from onyx_client.utils.mapper import init_device

_LOGGER = logging.getLogger(__name__)


class OnyxClient:
    """The ONYX.CENTER API Client.

    After initializing, call ::verify to check if:
      - the provided connection parameters are correct
      - the ONYX.CENTER supports the client's API version"""

    def __init__(self, config: Configuration, client_session: aiohttp.ClientSession):
        """Initialize the API client.

        config: the access configuration of the client
        client_session: the aiohttp session to use"""
        self.config = config
        self.url_helper = UrlHelper(config, client_session)
        self._shutdown = True
        self._readLoopTask = None
        self._eventLoop = asyncio.get_event_loop()
        self._activeTasks = set()
        self._event_callback = None

    async def supported_versions(self) -> Optional[SupportedVersions]:
        """Get all supported versions by the ONYX.CENTER."""
        data = await self.url_helper.perform_get_request("/versions", with_api=False)
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /versions.",
                self.config.fingerprint,
            )
            return None

        return SupportedVersions(data.get("versions", list()))

    async def verify(self) -> bool:
        """Check if the ONYX.CENTER supports the version
        and the connection parameters are working."""
        versions = await self.supported_versions()
        return versions.supports(API_VERSION) if versions is not None else False

    async def date_information(self) -> Optional[DateInformation]:
        """Get all date related information of the ONYX.CENTER."""
        data = await self.url_helper.perform_get_request("/clock")
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /clock.",
                self.config.fingerprint,
            )
            return None

        return DateInformation(
            float(data.get("time", "0")),
            data.get("zone", None),
            int(data.get("zone_offset", "0")),
        )

    async def devices(self, include_details: bool = False) -> Optional[list]:
        """Get all devices controlled by the ONYX.CENTER.

        include_details: ensures all device details are queried
                         before returning the device"""
        data = await self.url_helper.perform_get_request("/devices")
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /devices.",
                self.config.fingerprint,
            )
            return None

        if include_details:
            return [
                device
                for device in [await self.device(key) for key, _ in data.items()]
                if present(device)
            ]
        else:
            return [
                init_device(
                    key,
                    value.get("name", None),
                    DeviceType.convert(value.get("type", None)),
                )
                for key, value in data.items()
            ]

    async def device(self, identifier: str) -> Optional[Device]:
        """Get the device properties for a provided ID.

        identifier: the identifier of the device to query"""
        data = await self.url_helper.perform_get_request(f"/devices/{identifier}")
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /devices/%s.",
                self.config.fingerprint,
                identifier,
            )
            return None

        actions = [Action.convert(action) for action in data.get("actions", list())]
        return init_device(
            identifier,
            data.get("name", None),
            DeviceType.convert(data.get("type", None)),
            data.get("properties", None),
            actions,
            data,
        )

    async def send_command(self, identifier: str, command: DeviceCommand) -> bool:
        """Send a command to the device with the provided ID.

        identifier: the device identifier
        command: the command object to send to the device"""
        data = await self.url_helper.perform_post_request(
            f"/devices/{identifier}/command", command.data()
        )
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /devices/%s/command.",
                self.config.fingerprint,
                identifier,
            )
        return data is not None

    async def cancel_command(self, identifier: str) -> bool:
        """Cancel a command to the device with the provided ID.

        identifier: the device identifier to cancel the command for"""
        data = await self.url_helper.perform_delete_request(
            f"/devices/{identifier}/command"
        )
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /devices/%s/command.",
                self.config.fingerprint,
                identifier,
            )
        return data is not None

    async def groups(self) -> Optional[list]:
        """Get all groups controlled by the ONYX.CENTER."""
        data = await self.url_helper.perform_get_request("/groups")
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /groups.",
                self.config.fingerprint,
            )
            return None

        return [
            Group(key, value.get("name", None), value.get("devices", list()))
            for key, value in data.items()
        ]

    async def group(self, identifier: str) -> Optional[Group]:
        """Get the group properties for a provided ID.

        identifier: the group identifier to query"""
        data = await self.url_helper.perform_get_request(f"/groups/{identifier}")
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /groups/%s.",
                self.config.fingerprint,
                identifier,
            )
            return None

        return Group(identifier, data.get("name", None), data.get("devices", list()))

    async def send_group_command(self, identifier: str, command: DeviceCommand) -> bool:
        """Send a command to the group with the provided ID.

        identifier: the group identifier
        command: the command object to send to the group"""
        data = await self.url_helper.perform_post_request(
            f"/groups/{identifier}/command", command.data()
        )
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /groups/%s/command.",
                self.config.fingerprint,
                identifier,
            )
            return False

        unsuccessful = [
            key
            for (key, value) in data.get("results", dict()).items()
            if value.get("status_code", 501) != 200
        ]
        if len(unsuccessful) > 0:
            _LOGGER.error(
                "Could not execute command for all devices in group %s: %s",
                identifier,
                unsuccessful,
            )
        return len(unsuccessful) == 0

    async def cancel_group_command(self, identifier: str) -> bool:
        """Cancel a command to the group with the provided ID.

        identifier: the group identifier to cancel the command for"""
        data = await self.url_helper.perform_delete_request(
            f"/groups/{identifier}/command"
        )
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /groups/%s/command.",
                self.config.fingerprint,
                identifier,
            )
        return data is not None

    async def events(self, include_details: bool = False) -> Device:
        """Stream events continuously.

        include_details: ensures all device details are queried
                         before emiting the device"""
        async for message in self.url_helper.start_stream("/events"):
            if message is not None and len(message) > 0 and message.startswith("data:"):
                message = message[len("data:") :].strip()
                events = json.loads(message)
                for key, value in events.get("devices", dict()).items():
                    try:
                        if value is not None:
                            device = (
                                await self.device(key)
                                if include_details
                                else init_device(
                                    key,
                                    value.get("name", None),
                                    DeviceType.convert(value.get("type", None)),
                                    value.get("properties", None),
                                    value,
                                )
                            )
                            yield device
                    except AttributeError:
                        _LOGGER.error(
                            "Received unknown device data. Dropping device %s", key
                        )

    def start(self, include_details: bool = False, backoff_time: int = 1):
        """Start the event stream via callback.

        include_details: ensures all device details are queried
                         before emiting the device
        backoff_time: the maximum time in minutes for a connection retry"""
        self._shutdown = False
        self._readLoopTask = self._create_internal_task(
            self._read_handler(include_details, backoff_time), name="read_loop"
        )

    def stop(self):
        """Stop the event stream via callback."""
        self._shutdown = True

    def set_event_callback(self, callback):
        """Set the event stream callback.

        callback: the callback function taking the device as the only parameter"""
        self._event_callback = callback

    def _create_internal_task(self, coro, name=None):
        """Create an internal task running in the background.

        coro: the coroutine to run
        name: the event loop name"""
        task = self._eventLoop.create_task(coro, name=name)
        task.add_done_callback(self._complete_internal_task)
        self._activeTasks.add(task)

    async def _read_handler(self, include_details: bool = False, backoff_time: int = 1):
        """Handle rerunning the task in the background.

        include_details: ensures all device details are queried
                         before emiting the device
        backoff_time: the maximum time in minutes for a connection retry"""
        while not self._shutdown:
            try:
                await self._read_loop(include_details)
            except asyncio.CancelledError:
                raise
            except Exception as ex:
                backoff = int(uniform(0, backoff_time) * 60)
                _LOGGER.error(
                    "Unexpected exception: %r. Retrying with backoff %ds.", ex, backoff
                )
                await asyncio.sleep(backoff)

    def _complete_internal_task(self, task):
        """Remove an internal task that was running in the background.

        task: the task to remove"""
        self._activeTasks.remove(task)
        if not task.cancelled():
            ex = task.exception()
            _LOGGER.error("Unexpected exception: %r. Completing task.", ex)
            raise ex

    async def _read_loop(self, include_details: bool = False):
        """Streams data from the ONYX API endpoint and emits device updates.
        Updates are emitted as events through the event_callback.

        include_details: ensures all device details are queried
                         before emiting the device"""
        while not self._shutdown:
            async for device in self.events(include_details):
                if self._shutdown:
                    break
                if self._event_callback is not None:
                    _LOGGER.info("Received device: %s", device)
                    self._event_callback(device)
                else:
                    _LOGGER.warning("Received data but no callback is defined")


def create(
    config: Configuration = None,
    fingerprint: str = None,
    access_token: str = None,
    client_session: aiohttp.ClientSession = None,
) -> OnyxClient:
    """Create the client.

    Either config or fingerprint and access_token must be provided.

    config: the access configuration of the client (optional)
    fingerprint: the ONYX.CENTER fingerprint (optional)
    access_token: the access token to use (optional)
    client_session: the aiohttp session to use"""
    if config is None:
        config = Configuration(fingerprint, access_token)
    session = client_session if client_session is not None else aiohttp.ClientSession()
    return OnyxClient(config, session)
