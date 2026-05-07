"""DataUpdateCoordinators for Tisséo."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api_client import TisseoAPIError, TisseoAuthError, TisseoClient
from .const import DOMAIN, UPDATE_INTERVAL_FAST, UPDATE_INTERVAL_SLOW

_LOGGER = logging.getLogger(__name__)


class TisseoScheduleCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for stop schedules (fast updates)."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        client: TisseoClient,
        stops: list[dict],
    ) -> None:
        """Initialize."""
        self.client = client
        self.entry = entry
        self.stops = stops
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Tisséo",
            manufacturer="Tisséo",
            model="Open Data API",
        )

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_schedules",
            update_interval=timedelta(seconds=UPDATE_INTERVAL_FAST),
            always_update=True,
            config_entry=entry,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch schedule data."""
        if not self.stops:
            return {}

        stops_list = ",".join(stop["stop_id"] for stop in self.stops)
        try:
            return await self.client.get_stop_schedules(
                stops_list=stops_list,
                number=5,
                display_real_time=True,
                timetable_by_area=True,
            )
        except TisseoAuthError as err:
            raise UpdateFailed(f"Authentication failed: {err}") from err
        except TisseoAPIError as err:
            raise UpdateFailed(f"API error: {err}") from err


class TisseoInfoCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for lines, messages, and journey (slow updates)."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        client: TisseoClient,
        line_ids: list[str] | None = None,
        journey: dict[str, str] | None = None,
    ) -> None:
        """Initialize."""
        self.client = client
        self.entry = entry
        self.line_ids = line_ids or []
        self.journey = journey
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Tisséo",
            manufacturer="Tisséo",
            model="Open Data API",
        )

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_info",
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SLOW),
            always_update=True,
            config_entry=entry,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch lines, messages, and optional journey."""
        data: dict[str, Any] = {"lines": {}, "messages": [], "journey": None}

        try:
            lines_data = await self.client.get_lines(display_messages=True)
            raw_lines = lines_data.get("lines", {}).get("line", [])
            if isinstance(raw_lines, dict):
                raw_lines = [raw_lines]
            for line in raw_lines:
                line_id = line.get("id")
                if line_id:
                    data["lines"][line_id] = line

            messages_data = await self.client.get_messages()
            raw_messages = messages_data.get("messages", [])
            if isinstance(raw_messages, dict):
                raw_messages = [raw_messages]
            data["messages"] = raw_messages

            if self.journey:
                journey_data = await self.client.get_journeys(
                    departure_place=self.journey["journey_origin"],
                    arrival_place=self.journey["journey_destination"],
                    number=1,
                    display_wording=True,
                )
                data["journey"] = journey_data

        except TisseoAuthError as err:
            raise UpdateFailed(f"Authentication failed: {err}") from err
        except TisseoAPIError as err:
            raise UpdateFailed(f"API error: {err}") from err

        return data
