"""Onyx Client API class."""

import asyncio
import json
import logging
import time
from collections.abc import AsyncGenerator
from contextlib import aclosing
from urllib.parse import quote

import aiohttp

from .configuration.configuration import Configuration
from .data.automation import Automation
from .data.date_information import DateInformation
from .data.device_command import DeviceCommand
from .data.supported_versions import SupportedVersions
from .data.update_status import UpdateStatus
from .device.device import Device
from .enum.verify_result import VerifyResult
from .exception.invalid_stream_data import InvalidStreamDataException
from .group.group import Group
from .helpers.url import UrlHelper
from .stream.events import Event, Pulse, Resynced, Snapshot
from .stream.sse import parse
from .stream.state import State
from .utils.const import (
    API_VERSION,
    CLOCK_TIMEOUT,
    DEPRECATED_API_VERSION,
    STREAM_MAX_BACKOFF,
)
from .utils.mapper import init_device, init_group
from .utils.sanitize import describe_exception, protect

_LOGGER = protect(logging.getLogger(__name__))


class OnyxClient:
    """The ONYX.CENTER API Client.

    After initializing, call ::verify to check if:
      - the provided connection parameters are correct
      - the ONYX.CENTER supports the client's API version

    The client never runs background tasks: ::stream only runs while iterated."""

    def __init__(self, config: Configuration, client_session: aiohttp.ClientSession):
        """Initialize the API client.

        config: the access configuration of the client
        client_session: the aiohttp session to use"""
        self.config = config
        self.client_session = client_session
        self.url_helper = UrlHelper(config, client_session)
        self.clock_offset = 0.0
        self._close_session = False
        self._resync_requested = False
        self._closed = False
        if config.api_version == DEPRECATED_API_VERSION:
            # pragma: no mutate start
            _LOGGER.warning(
                "ONYX API %s is deprecated and will be removed in onyx-client 13.0.0, use %s.",
                DEPRECATED_API_VERSION,
                API_VERSION,
            )
            # pragma: no mutate end

    async def __aenter__(self):
        """Enter async context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context manager and close resources."""
        await self.close()

    async def close(self):
        """Stop the stream and close the client session if the client created it."""
        self._closed = True
        self.url_helper.close_stream()
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

    async def verify(self) -> VerifyResult:
        """Check if the ONYX.CENTER supports the configured API version
        and the connection parameters are working."""
        try:
            versions = await self.supported_versions()
            if versions is None:
                return VerifyResult.UNREACHABLE
            if not versions.supports(self.config.api_version):
                return VerifyResult.VERSION_UNSUPPORTED
            status = await self.url_helper.perform_status_request("GET", "/clock")
        except (aiohttp.ClientError, TimeoutError):
            return VerifyResult.UNREACHABLE
        if status in (401, 403):
            return VerifyResult.UNAUTHORIZED
        return VerifyResult.OK if status == 200 else VerifyResult.UNREACHABLE

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

    async def devices(self) -> list | None:
        """Get all devices controlled by the ONYX.CENTER.

        The devices only contain the summary data; use ::device for the
        properties."""
        data = await self.url_helper.perform_get_request("/devices")
        if data is None:
            # pragma: no mutate start
            _LOGGER.error(
                "Could not call ONYX API for device %s: /devices.",
                self.config.identifier,
            )
            # pragma: no mutate end
            return None

        return [init_device(key, value) for key, value in data.items()]

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

        return init_device(identifier, data)

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

        return [init_group(key, value) for key, value in data.items()]

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

        return init_group(identifier, data)

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

    async def automations(self) -> list | None:
        """Get all automations configured on the ONYX.CENTER (API v6)."""
        data = await self.url_helper.perform_get_request("/automations")
        if data is None:
            # pragma: no mutate start
            _LOGGER.error(
                "Could not call ONYX API for device %s: /automations.",
                self.config.identifier,
            )
            # pragma: no mutate end
            return None

        return [Automation.create(value) for value in data]

    async def enable_automation(self, identifier: str) -> Automation | None:
        """Enable the automation with the provided ID (API v6).

        identifier: the automation identifier"""
        return await self._switch_automation(identifier, "enable")

    async def disable_automation(self, identifier: str) -> Automation | None:
        """Disable the automation with the provided ID (API v6).

        Disabling also cancels the commands the automation issued.

        identifier: the automation identifier"""
        return await self._switch_automation(identifier, "disable")

    async def _switch_automation(
        self, identifier: str, action: str
    ) -> Automation | None:
        """Enable or disable the automation with the provided ID.

        identifier: the automation identifier
        action: enable or disable"""
        path = f"/automations/{quote(identifier, safe='')}/{action}"
        data = await self.url_helper.perform_post_request(path)
        if data is None:
            # pragma: no mutate start
            _LOGGER.error(
                "Could not call ONYX API for device %s: %s.",
                self.config.identifier,
                path,
            )
            # pragma: no mutate end
            return None

        return Automation.create(data)

    async def update_status(self) -> UpdateStatus | None:
        """Get the installed and available software version (API v6)."""
        data = await self.url_helper.perform_get_request("/update")
        if data is None:
            # pragma: no mutate start
            _LOGGER.error(
                "Could not call ONYX API for device %s: /update.",
                self.config.identifier,
            )
            # pragma: no mutate end
            return None

        return UpdateStatus.create(data)

    async def check_for_update(self) -> UpdateStatus | None:
        """Check for a new software version and return the status (API v6).

        Blocks until the check is complete; fails if the ONYX.CENTER is offline."""
        return await self._post_update("/update/check")

    async def install_update(self) -> UpdateStatus | None:
        """Install the available software update (API v6).

        The ONYX.CENTER restarts, which closes the stream until it is back."""
        return await self._post_update("/update/install")

    async def _post_update(self, path: str) -> UpdateStatus | None:
        """Perform an update request.

        path: the URL path"""
        data = await self.url_helper.perform_post_request(path)
        if data is None:
            # pragma: no mutate start
            _LOGGER.error(
                "Could not call ONYX API for device %s: %s.",
                self.config.identifier,
                path,
            )
            # pragma: no mutate end
            return None

        return UpdateStatus.create(data)

    async def logout(self) -> bool:
        """Revoke the access token (API v6).

        Returns True if the token is invalid afterwards and False if the
        ONYX.CENTER could not revoke it."""
        status = await self.url_helper.perform_status_request("POST", "/logout")
        return status in (204, 401)

    def now(self) -> float:
        """Get the ONYX.CENTER time as UNIX timestamp.

        ::clock_offset is measured on every (re)connect of ::stream (0 before).
        Use it to evaluate animations, e.g. NumericValue.effective_value."""
        return time.time() + self.clock_offset

    async def stream(self) -> AsyncGenerator[Event, None]:
        """Stream the state of the ONYX.CENTER as events.

        Every (re)connect yields a Snapshot with the complete state. After a
        reconnect, Resynced precedes it and the differences to the previous
        state follow it. Patches yield DeviceAdded, DeviceChanged,
        DeviceRemoved, GroupsChanged, AutomationsChanged and UpdateChanged with
        complete objects; heartbeats yield Pulse.

        Errors, including a silent stream, reconnect with an exponential
        backoff. Rejected credentials (HTTP 401/403) raise
        aiohttp.ClientResponseError without the request headers, so it never
        carries the access token. Before every connect the clock offset is
        refreshed (for at most CLOCK_TIMEOUT seconds; the previous offset is
        kept on failure). Resynced.reason never contains credentials. Runs until the caller stops iterating or
        ::close was called (effective at the next message or reconnect); close
        the generator (e.g. contextlib.aclosing) to release the connection
        immediately."""
        state = State()
        attempt = 0
        reason = None
        while not self._closed:
            self._resync_requested = False
            try:
                await self._update_clock_offset()
                async with aclosing(self._connect(state, reason)) as events:
                    async for event in events:
                        if isinstance(event, Snapshot):
                            attempt = 0
                        yield event
                reason = "stream closed"
            except aiohttp.ClientResponseError as ex:
                if ex.status in (401, 403):
                    raise
                reason = describe_exception(ex)
            except (
                aiohttp.ClientError,
                TimeoutError,
                InvalidStreamDataException,
            ) as ex:
                reason = describe_exception(ex)
            if self._closed:
                return
            if self._resync_requested:
                reason = "resync requested"
                continue
            delay = min(2**attempt, STREAM_MAX_BACKOFF)
            attempt += 1
            # pragma: no mutate start
            _LOGGER.warning(
                "ONYX event stream of %s ended (%s), reconnecting in %ds.",
                self.config.identifier,
                reason,
                delay,
            )
            # pragma: no mutate end
            await asyncio.sleep(delay)

    def resync(self):
        """Reconnect a running ::stream; its new snapshot replaces the state."""
        self._resync_requested = True
        self.url_helper.close_stream()

    async def _connect(
        self, state: State, reason: str | None
    ) -> AsyncGenerator[Event, None]:
        """Connect to the event stream and yield its events.

        Raises InvalidStreamDataException if the data cannot be processed.

        state: the state store
        reason: why the stream reconnects"""
        snapshot_received = False
        async with (
            aclosing(self.url_helper.start_stream("/events")) as lines,
            aclosing(parse(lines)) as messages,
        ):
            async for event, data in messages:
                if self._resync_requested or self._closed:
                    return
                try:
                    if event == "snapshot":
                        resynced = not snapshot_received and state.data is not None
                        items = state.replace(json.loads(data))
                        if resynced:
                            items.insert(0, Resynced(reason))
                        snapshot_received = True
                    elif event == "patch" and snapshot_received:
                        items = state.apply(json.loads(data))
                    elif event == "patch":
                        raise ValueError("PATCH_BEFORE_SNAPSHOT")
                    elif event == "pulse":
                        items = [Pulse(float(data))]
                    else:
                        continue
                except (ValueError, TypeError, AttributeError) as ex:
                    raise InvalidStreamDataException(repr(ex)[:200]) from ex
                for item in items:
                    yield item

    async def _update_clock_offset(self):
        """Update ::clock_offset from the ONYX.CENTER clock.

        The clock is best-effort and never blocks or aborts a connect: it is
        given CLOCK_TIMEOUT seconds only; when it does not answer, is not
        reachable or sends invalid data, the previous offset is kept. Only
        rejected credentials (HTTP 401/403) are raised."""
        before = time.time()
        try:
            async with asyncio.timeout(CLOCK_TIMEOUT):
                info = await self.date_information()
        except TimeoutError as ex:
            # pragma: no mutate start
            _LOGGER.warning(
                "ONYX clock of %s timed out (%s), keeping the offset.",
                self.config.identifier,
                describe_exception(ex),
            )
            # pragma: no mutate end
            return
        except aiohttp.ClientError as ex:
            if isinstance(ex, aiohttp.ClientResponseError) and ex.status in (401, 403):
                raise
            # pragma: no mutate start
            _LOGGER.warning(
                "ONYX clock of %s failed (%s), keeping the offset.",
                self.config.identifier,
                describe_exception(ex),
            )
            # pragma: no mutate end
            return
        except (ValueError, TypeError, AttributeError) as ex:
            # pragma: no mutate start
            _LOGGER.warning(
                "ONYX clock of %s sent invalid data (%s), keeping the offset.",
                self.config.identifier,
                describe_exception(ex),
            )
            # pragma: no mutate end
            return
        if info is not None and info.time > 0:
            self.clock_offset = info.time - (before + time.time()) / 2


def create(
    config: Configuration = None,
    fingerprint: str | None = None,
    access_token: str | None = None,
    local_address: str | None = None,
    client_session: aiohttp.ClientSession = None,
    api_version: str = API_VERSION,
) -> OnyxClient:
    """Create the client.

    Either config or fingerprint and access_token must be provided.

    config: the access configuration of the client (optional)
    fingerprint: the ONYX.CENTER fingerprint (optional)
    access_token: the access token to use (optional)
    local_address: the local address to use (optional)
    client_session: the aiohttp session to use
    api_version: the API version to use without config (default: v6, deprecated: v3)"""
    if config is None:
        config = Configuration(
            fingerprint,
            access_token,
            local_address=local_address,
            api_version=api_version,
        )
    session = client_session if client_session is not None else aiohttp.ClientSession()
    client = OnyxClient(config, session)
    client._close_session = client_session is None
    return client
