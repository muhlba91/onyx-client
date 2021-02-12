"""Onyx Client API class."""
import logging
from typing import Any, Optional

import aiohttp

from onyx_client.configuration.configuration import Configuration
from onyx_client.data.boolean_value import BooleanValue
from onyx_client.data.date_information import DateInformation
from onyx_client.data.device_command import DeviceCommand
from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.data.supported_versions import SupportedVersions
from onyx_client.device.device import Device
from onyx_client.device.shutter import Shutter
from onyx_client.device.weather import Weather
from onyx_client.enum.action import Action
from onyx_client.enum.device_type import DeviceType
from onyx_client.group.group import Group
from onyx_client.utils.const import API_HEADERS, API_URL, API_VERSION
from onyx_client.utils.filter import present

_LOGGER = logging.getLogger(__name__)


class OnyxClient:
    """The ONYX.CENTER API Client.

    After initializing, call ::verify to check if:
      - the provided connection parameters are correct
      - the ONYX.CENTER supports the client's API version"""

    def __init__(self, config: Configuration, client_session: aiohttp.ClientSession):
        """Initialize the API client."""
        self.config = config
        self.client_session = client_session

    @staticmethod
    async def authorize(
        code: str, client_session: aiohttp.ClientSession
    ) -> Optional[Configuration]:
        """Authorize the client using an API code."""
        async with client_session.post(
            f"{API_URL}/authorize",
            data={"code": code},
            headers=API_HEADERS,
        ) as response:
            if not OnyxClient._check_response(response):
                _LOGGER.error("Could not authorize client for ONYX API.")
                return None
            data = await response.json()
            return Configuration(data["fingerprint"], data["token"])

    @property
    def _headers(self) -> dict:
        """Get all common headers."""
        return {"Authorization": f"Bearer {self.config.access_token}", **API_HEADERS}

    def _base_url(self, with_api: bool = True) -> str:
        """Get the API base URL for this ONYX.CENTER."""
        api = f"{API_URL}/box/{self.config.fingerprint}/api"
        if with_api:
            api = f"{api}/{API_VERSION}"
        return api

    def _url(self, path: str = "", with_api: bool = True) -> str:
        """Get the request URL."""
        return f"{self._base_url(with_api=with_api)}{path}"

    @staticmethod
    def _check_response(response: aiohttp.ClientResponse) -> bool:
        """Check the response for a success HTTP status code.

        Success codes are:
          - 200"""
        if response.status == 200:
            _LOGGER.debug("Received HTTP response from ONYX API: %s", response.status)
            return True
        else:
            _LOGGER.error(
                "Received erroneous HTTP response from ONYX API: %s", response.status
            )
            return False

    @staticmethod
    def _init_device(
        identifier: str,
        name: str,
        device_type: DeviceType,
        properties: dict = None,
        actions: list = None,
    ) -> Device:
        """Initialize the device correctly."""
        device_mode_value = (
            DeviceType.convert(properties["device_type"]["type"])
            if properties is not None
            else device_type
        )
        device_mode_values = (
            [DeviceType.convert(value) for value in properties["device_type"]["values"]]
            if properties is not None
            else None
        )
        device_mode = DeviceMode(device_mode_value, device_mode_values)
        if device_type.is_shutter():
            target_position = (
                NumericValue.create(properties["target_position"])
                if properties is not None
                else None
            )
            target_angle = (
                NumericValue.create(properties["target_angle"])
                if properties is not None
                else None
            )
            actual_angle = (
                NumericValue.create(properties["actual_angle"])
                if properties is not None
                else None
            )
            actual_position = (
                NumericValue.create(properties["actual_position"])
                if properties is not None
                else None
            )
            drivetime_down = (
                NumericValue.create(properties["drivetime_down"])
                if properties is not None
                else None
            )
            drivetime_up = (
                NumericValue.create(properties["drivetime_up"])
                if properties is not None
                else None
            )
            rotationtime = (
                NumericValue.create(properties["rotationtime"])
                if properties is not None
                else None
            )
            switch_button_direction = (
                BooleanValue.create(properties["switch_button_direction"])
                if properties is not None
                else None
            )
            switch_drive_direction = (
                BooleanValue.create(properties["switch_drive_direction"])
                if properties is not None
                else None
            )
            return Shutter(
                identifier,
                name,
                device_type,
                device_mode,
                actions,
                target_position,
                target_angle,
                actual_angle,
                actual_position,
                drivetime_down,
                drivetime_up,
                rotationtime,
                switch_button_direction,
                switch_drive_direction,
            )
        elif device_type == DeviceType.WEATHER:
            wind_peak = (
                NumericValue.create(properties["wind_peak"])
                if properties is not None
                else None
            )
            sun_brightness_peak = (
                NumericValue.create(properties["sun_brightness_peak"])
                if properties is not None
                else None
            )
            sun_brightness_sink = (
                NumericValue.create(properties["sun_brightness_sink"])
                if properties is not None
                else None
            )
            air_pressure = (
                NumericValue.create(properties["air_pressure"])
                if properties is not None
                else None
            )
            humidity = (
                NumericValue.create(properties["humidity"])
                if properties is not None
                else None
            )
            temperature = (
                NumericValue.create(properties["temperature"])
                if properties is not None
                else None
            )
            return Weather(
                identifier,
                name,
                device_type,
                device_mode,
                actions,
                wind_peak,
                sun_brightness_peak,
                sun_brightness_sink,
                air_pressure,
                humidity,
                temperature,
            )
        else:
            return Device(identifier, name, device_type, device_mode, actions)

    async def _perform_get_request(
        self, path: str, with_api: bool = True
    ) -> Optional[Any]:
        """Perform a GET request."""
        async with self.client_session.get(
            self._url(path, with_api=with_api), headers=self._headers
        ) as response:
            if not self._check_response(response):
                return None
            return await response.json()

    async def _perform_delete_request(self, path: str) -> Optional[Any]:
        """Perform a DELETE request."""
        async with self.client_session.delete(
            self._url(path), headers=self._headers
        ) as response:
            if not self._check_response(response):
                return None
            return await response.json()

    async def _perform_post_request(self, path: str, data: dict) -> Optional[Any]:
        """Perform a POST request."""
        async with self.client_session.post(
            self._url(path), json=data, headers=self._headers
        ) as response:
            if not self._check_response(response):
                return None
            return await response.json()

    async def supported_versions(self) -> Optional[SupportedVersions]:
        """Get all supported versions by the ONYX.CENTER."""
        data = await self._perform_get_request("/versions", with_api=False)
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /versions.",
                self.config.fingerprint,
            )
            return None

        return SupportedVersions(data["versions"])

    async def verify(self) -> bool:
        """Check if the ONYX.CENTER supports the version
        and the connection parameters are working."""
        versions = await self.supported_versions()
        return versions.supports(API_VERSION) if versions is not None else False

    async def date_information(self) -> Optional[DateInformation]:
        """Get all date related information of the ONYX.CENTER."""
        data = await self._perform_get_request("/clock")
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /clock.",
                self.config.fingerprint,
            )
            return None

        return DateInformation(
            float(data["time"]), data["zone"], int(data["zone_offset"])
        )

    async def devices(self, include_details: bool = False) -> Optional[list]:
        """Get all devices controlled by the ONYX.CENTER."""
        data = await self._perform_get_request("/devices")
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
                self._init_device(key, value["name"], DeviceType.convert(value["type"]))
                for key, value in data.items()
            ]

    async def device(self, identifier: str) -> Optional[Device]:
        """Get the device properties for a provided ID."""
        data = await self._perform_get_request(f"/devices/{identifier}")
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /devices/%s.",
                self.config.fingerprint,
                identifier,
            )
            return None

        actions = (
            [Action.convert(action) for action in data["actions"]]
            if "actions" in data
            else None
        )
        return self._init_device(
            identifier,
            data["name"],
            DeviceType.convert(data["type"]),
            data["properties"],
            actions,
        )

    async def send_command(self, identifier: str, command: DeviceCommand) -> bool:
        """Send a command to the device with the provided ID."""
        data = await self._perform_post_request(
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
        """Cancel a command to the device with the provided ID."""
        data = await self._perform_delete_request(f"/devices/{identifier}/command")
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /devices/%s/command.",
                self.config.fingerprint,
                identifier,
            )
        return data is not None

    async def groups(self) -> Optional[list]:
        """Get all groups controlled by the ONYX.CENTER."""
        data = await self._perform_get_request("/groups")
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /groups.",
                self.config.fingerprint,
            )
            return None

        return [
            Group(key, value["name"], value["devices"]) for key, value in data.items()
        ]

    async def group(self, identifier: str) -> Optional[Group]:
        """Get the group properties for a provided ID."""
        data = await self._perform_get_request(f"/groups/{identifier}")
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /groups/%s.",
                self.config.fingerprint,
                identifier,
            )
            return None

        return Group(identifier, data["name"], data["devices"])

    async def send_group_command(self, identifier: str, command: DeviceCommand) -> bool:
        """Send a command to the group with the provided ID."""
        data = await self._perform_post_request(
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
            for (key, value) in data["results"].items()
            if value["status_code"] != 200
        ]
        if len(unsuccessful) > 0:
            _LOGGER.error(
                "Could not execute command for all devices in group %s: %s",
                identifier,
                unsuccessful,
            )
        return len(unsuccessful) == 0

    async def cancel_group_command(self, identifier: str) -> bool:
        """Cancel a command to the group with the provided ID."""
        data = await self._perform_delete_request(f"/groups/{identifier}/command")
        if data is None:
            _LOGGER.error(
                "Could not call ONYX API for device %s: /groups/%s/command.",
                self.config.fingerprint,
                identifier,
            )
        return data is not None
