"""Onyx Client API class."""

import asyncio
import json
import logging
from collections.abc import AsyncGenerator
from random import uniform

import aiohttp

from .configuration.configuration import Configuration
from .data.date_information import DateInformation
from .data.device_command import DeviceCommand
from .data.supported_versions import SupportedVersions
from .device.device import Device
from .enum.action import Action
from .enum.device_type import DeviceType
from .group.group import Group
from .helpers.url import UrlHelper
from .utils.const import API_VERSION
from .utils.filter import present
from .utils.mapper import init_device

_LOGGER = logging.getLogger(__name__)


class OnyxClient:
    """The ONYX.CENTER API Client.

    After initializing, call ::verify to check if:
      - the provided connection parameters are correct
      - the ONYX.CENTER supports the client's API version"""

    def __init__(
        self,
        config: Configuration,
        client_session: aiohttp.ClientSession,
        event_loop: asyncio.AbstractEventLoop | None = None,
    ):
        """Initialize the API client.

        config: the access configuration of the client
        client_session: the aiohttp session to use
        event_loop: the event loop to use for background events"""
        self.config = config
        self.client_session = client_session
        self.url_helper = UrlHelper(config, client_session)
        self._shutdown = True
        self._read_loop_task = None
        self._close_session = False
        if event_loop is not None:
            self._event_loop = event_loop
        else:
            try:
                self._event_loop = asyncio.get_running_loop()
            except RuntimeError:
                self._event_loop = None
        self._active_tasks = set()
        self._event_callback = None

    async def __aenter__(self):
        """Enter async context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context manager and close resources."""
        await self.close()

    async def close(self):
        """Close client connections and cancel any background tasks."""
        self.stop()
        if (
            self._close_session
            and self.client_session is not None
            and not self.client_session.closed
        ):
            await self.client_session.close()

    async def supported_versions(self) -> SupportedVersions | None:
        """Get all supported versions by the ONYX.CENTER."""
        # pragma: no mutate start
        data = await self.url_helper.perform_get_request("/versions", with_api=False)
        # pragma: no mutate end
        if data is None:
            # pragma: no mutate start
            _LOGGER.error(
                "Could not call ONYX API for device %s: /versions.",
                self.config.identifier,
            )
            # pragma: no mutate end
            return None

        return SupportedVersions(data.get("versions", []))

    async def verify(self) -> bool:
        """Check if the ONYX.CENTER supports the version
        and the connection parameters are working."""
        versions = await self.supported_versions()
        return versions.supports(API_VERSION) if versions is not None else False

    async def date_information(self) -> DateInformation | None:
        """Get all date related information of the ONYX.CENTER."""
        data = await self.url_helper.perform_get_request("/clock")
        if data is None:
            # pragma: no mutate start
            _LOGGER.error(
                "Could not call ONYX API for device %s: /clock.",
                self.config.identifier,
            )
            # pragma: no mutate end
            return None

        return DateInformation(
            float(data.get("time", "0")),
            data.get("zone"),
            int(data.get("zone_offset", "0")),
        )

    async def devices(self, include_details: bool = False) -> list | None:
        """Get all devices controlled by the ONYX.CENTER.

        include_details: ensures all device details are queried
                         before returning the device"""
        data = await self.url_helper.perform_get_request("/devices")
        if data is None:
            # pragma: no mutate start
            _LOGGER.error(
                "Could not call ONYX API for device %s: /devices.",
                self.config.identifier,
            )
            # pragma: no mutate end
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
                    value.get("name"),
                    DeviceType.convert(value.get("type")),
                )
                for key, value in data.items()
            ]

    async def device(self, identifier: str) -> Device | None:
        """Get the device properties for a provided ID.

        identifier: the identifier of the device to query"""
        data = await self.url_helper.perform_get_request(f"/devices/{identifier}")
        if data is None:
            # pragma: no mutate start
            _LOGGER.error(
                "Could not call ONYX API for device %s: /devices/%s.",
                self.config.identifier,
                identifier,
            )
            # pragma: no mutate end
            return None

        actions = [Action.convert(action) for action in data.get("actions", [])]
        return init_device(
            identifier,
            data.get("name"),
            DeviceType.convert(data.get("type")),
            data.get("properties"),
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
        # pragma: no mutate start
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /devices/%s/command.",
                self.config.identifier,
                identifier,
            )
        # pragma: no mutate end
        return data is not None

    async def cancel_command(self, identifier: str) -> bool:
        """Cancel a command to the device with the provided ID.

        identifier: the device identifier to cancel the command for"""
        data = await self.url_helper.perform_delete_request(
            f"/devices/{identifier}/command"
        )
        # pragma: no mutate start
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /devices/%s/command.",
                self.config.identifier,
                identifier,
            )
        # pragma: no mutate end
        return data is not None

    async def groups(self) -> list | None:
        """Get all groups controlled by the ONYX.CENTER."""
        data = await self.url_helper.perform_get_request("/groups")
        if data is None:
            # pragma: no mutate start
            _LOGGER.error(
                "Could not call ONYX API for device %s: /groups.",
                self.config.identifier,
            )
            # pragma: no mutate end
            return None

        return [
            Group(key, value.get("name"), value.get("devices", []))
            for key, value in data.items()
        ]

    async def group(self, identifier: str) -> Group | None:
        """Get the group properties for a provided ID.

        identifier: the group identifier to query"""
        data = await self.url_helper.perform_get_request(f"/groups/{identifier}")
        if data is None:
            # pragma: no mutate start
            _LOGGER.error(
                "Could not call ONYX API for device %s: /groups/%s.",
                self.config.identifier,
                identifier,
            )
            # pragma: no mutate end
            return None

        return Group(identifier, data.get("name"), data.get("devices", []))

    async def send_group_command(self, identifier: str, command: DeviceCommand) -> bool:
        """Send a command to the group with the provided ID.

        identifier: the group identifier
        command: the command object to send to the group"""
        data = await self.url_helper.perform_post_request(
            f"/groups/{identifier}/command", command.data()
        )
        if data is None:
            # pragma: no mutate start
            _LOGGER.error(
                "Could not call ONYX API for device %s: /groups/%s/command.",
                self.config.identifier,
                identifier,
            )
            # pragma: no mutate end
            return False

        # pragma: no mutate start
        unsuccessful = [
            key
            for (key, value) in data.get("results", {}).items()
            if value.get("status_code", 501) != 200
        ]
        if len(unsuccessful) > 0:
            _LOGGER.error(
                "Could not execute command for all devices in group %s: %s",
                identifier,
                unsuccessful,
            )
        # pragma: no mutate end
        return len(unsuccessful) == 0

    async def cancel_group_command(self, identifier: str) -> bool:
        """Cancel a command to the group with the provided ID.

        identifier: the group identifier to cancel the command for"""
        data = await self.url_helper.perform_delete_request(
            f"/groups/{identifier}/command"
        )
        # pragma: no mutate start
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /groups/%s/command.",
                self.config.identifier,
                identifier,
            )
        # pragma: no mutate end
        return data is not None

    async def events(
        self, include_details: bool = False
    ) -> AsyncGenerator[Device | None, None]:
        """Stream events continuously.

        include_details: ensures all device details are queried
                         before emiting the device"""
        # pragma: no mutate start
        event = ""
        # pragma: no mutate end
        async for message in self.url_helper.start_stream("/events"):
            if message is not None and len(message) > 0:  # pragma: no mutate
                if message.startswith("event:"):
                    event = message[len("event:") :].strip()
                elif message.startswith("data:") and event in ["snapshot", "patch"]:
                    data = json.loads(message[len("data:") :].strip())
                    for key, value in data.get("devices", {}).items():
                        try:
                            if value is not None:
                                device = (
                                    await self.device(key)
                                    if include_details
                                    else init_device(
                                        key,
                                        value.get("name"),
                                        DeviceType.convert(value.get("type")),
                                        value.get("properties"),
                                        [
                                            Action.convert(action)
                                            for action in value.get("actions", [])
                                        ],
                                        value,
                                    )
                                )
                                yield device
                        except AttributeError:
                            # pragma: no mutate start
                            _LOGGER.error(
                                "Received unknown device data. Dropping device %s",
                                key,
                            )
                            # pragma: no mutate end

    # pragma: no mutate start
    def start(self, include_details: bool = False, backoff_time: int = 1):
        """Start the event stream via callback.

        include_details: ensures all device details are queried
                         before emiting the device
        backoff_time: the maximum time in minutes for a connection retry"""
        self._shutdown = False
        self._read_loop_task = self._create_internal_task(
            self._read_handler(include_details, backoff_time), name="read_loop"
        )

    def stop(self):
        """Stop the event stream via callback."""
        self._shutdown = True
        if self._read_loop_task is not None and not self._read_loop_task.done():
            self._read_loop_task.cancel()
            self._read_loop_task = None

    # pragma: no mutate end

    def set_event_callback(self, callback):
        """Set the event stream callback.

        callback: the callback function taking the device as the only parameter"""
        self._event_callback = callback

    # pragma: no mutate start
    def _create_internal_task(self, coro, name=None):
        """Create an internal task running in the background.

        coro: the coroutine to run
        name: the event loop name"""
        loop = self._event_loop or asyncio.get_running_loop()
        task = loop.create_task(coro, name=name)
        task.add_done_callback(self._complete_internal_task)
        self._active_tasks.add(task)
        return task

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
            except Exception as ex:  # noqa: BLE001
                backoff = int(uniform(0, backoff_time) * 60)
                _LOGGER.error(
                    "Unexpected exception: %r. Retrying with backoff %ds.", ex, backoff
                )
                await asyncio.sleep(backoff)

    def _complete_internal_task(self, task):
        """Remove an internal task that was running in the background.

        task: the task to remove"""
        self._active_tasks.discard(task)
        if not task.cancelled():
            ex = task.exception()
            if ex is not None:
                _LOGGER.error("Unexpected exception: %r. Completing task.", ex)
                raise ex
            else:
                _LOGGER.debug("Internal task completed without exception: %s", task)

    # pragma: no mutate end

    # pragma: no mutate start
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
                    _LOGGER.debug("Received device: %s", device)
                    self._event_callback(device)
                else:
                    _LOGGER.warning("Received data but no callback is defined.")

    # pragma: no mutate end


def create(
    config: Configuration = None,
    fingerprint: str | None = None,
    access_token: str | None = None,
    local_address: str | None = None,
    client_session: aiohttp.ClientSession = None,
    event_loop=None,
) -> OnyxClient:
    """Create the client.

    Either config or fingerprint and access_token must be provided.

    config: the access configuration of the client (optional)
    fingerprint: the ONYX.CENTER fingerprint (optional)
    access_token: the access token to use (optional)
    local_address: the local address to use (optional)
    client_session: the aiohttp session to use
    event_loop: the event loop to use for background events"""
    if config is None:
        config = Configuration(fingerprint, access_token, local_address=local_address)
    session = client_session if client_session is not None else aiohttp.ClientSession()
    client = OnyxClient(config, session, event_loop)
    client._close_session = client_session is None
    return client
