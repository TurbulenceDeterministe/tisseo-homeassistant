"""Sensor platform for Tisséo."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import (
    CONF_JOURNEY_DESTINATION,
    CONF_JOURNEY_ORIGIN,
    CONF_STOP_ID,
    CONF_STOP_NAME,
    DOMAIN,
)
from .coordinator import TisseoInfoCoordinator, TisseoScheduleCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors."""
    data = hass.data[DOMAIN][entry.entry_id]
    schedule_coordinator: TisseoScheduleCoordinator = data["schedule_coordinator"]
    info_coordinator: TisseoInfoCoordinator = data["info_coordinator"]
    stops = data["stops"]
    journey = data["journey"]

    entities: list[SensorEntity] = []

    for stop in stops:
        entities.append(TisseoStopSensor(schedule_coordinator, stop, entry))

    entities.append(TisseoMessagesSensor(info_coordinator, entry))

    if journey:
        entities.append(TisseoJourneySensor(info_coordinator, entry, journey))

    async_add_entities(entities)


class TisseoStopSensor(CoordinatorEntity[TisseoScheduleCoordinator], SensorEntity):
    """Sensor for stop schedules."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:bus-stop"

    def __init__(
        self,
        coordinator: TisseoScheduleCoordinator,
        stop: dict,
        entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._stop = stop
        self._stop_id = stop[CONF_STOP_ID]
        self._stop_name = stop[CONF_STOP_NAME]
        self._attr_unique_id = f"{entry.entry_id}_stop_{self._stop_id}"
        self._attr_name = f"Arrêt {self._stop_name}"
        self._attr_device_info = coordinator.device_info

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle update."""
        data = self.coordinator.data
        if not data or "stopAreas" not in data:
            self._attr_native_value = None
            self._attr_extra_state_attributes = {}
            self.async_write_ha_state()
            return

        schedules: list[dict[str, Any]] = []
        stop_areas = data.get("stopAreas", [])
        if isinstance(stop_areas, dict):
            stop_areas = [stop_areas]
        for stop_area in stop_areas:
            if stop_area.get("id") != self._stop_id:
                continue
            raw_schedules = stop_area.get("schedules", [])
            if isinstance(raw_schedules, dict):
                raw_schedules = [raw_schedules]
            for sched in raw_schedules:
                line = sched.get("line", {})
                destination = sched.get("destination", {})
                raw_journeys = sched.get("journeys", [])
                if isinstance(raw_journeys, dict):
                    raw_journeys = [raw_journeys]
                next_times = []
                for j in raw_journeys:
                    rt = j.get("realTime")
                    next_times.append(
                        {
                            "datetime": j.get("dateTime"),
                            "realtime": rt in ("1", "yes"),
                            "waiting_time": j.get("waiting_time"),
                        }
                    )
                schedules.append(
                    {
                        "line_short_name": line.get("shortName"),
                        "line_name": line.get("name"),
                        "line_color": line.get("bgXmlColor"),
                        "destination": destination.get("name"),
                        "next_departures": next_times,
                    }
                )

        all_times: list[tuple[str, dict]] = []
        for sched in schedules:
            for dep in sched["next_departures"]:
                if dep["datetime"]:
                    all_times.append((dep["datetime"], sched))

        if all_times:
            all_times.sort(key=lambda x: x[0])
            dt_str = all_times[0][0]
            dt_parsed = self._parse_datetime(dt_str)
            if dt_parsed:
                self._attr_native_value = dt_parsed
            else:
                self._attr_native_value = dt_str
        else:
            self._attr_native_value = None

        self._attr_extra_state_attributes = {
            "schedules": schedules,
            "stop_name": self._stop_name,
            "stop_id": self._stop_id,
        }
        self.async_write_ha_state()

    @staticmethod
    def _parse_datetime(dt_str: str) -> datetime | None:
        """Parse API datetime string to timezone-aware datetime."""
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
            try:
                dt_naive = datetime.strptime(dt_str, fmt)
            except ValueError:
                continue
            paris_tz = dt_util.get_time_zone("Europe/Paris")
            if paris_tz:
                return dt_naive.replace(tzinfo=paris_tz)
            return dt_naive
        return None


class TisseoMessagesSensor(CoordinatorEntity[TisseoInfoCoordinator], SensorEntity):
    """Sensor for network messages."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:alert-circle-outline"
    _attr_name = "Messages réseau"
    _attr_translation_key = "messages"

    def __init__(self, coordinator: TisseoInfoCoordinator, entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_messages"
        self._attr_device_info = coordinator.device_info

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle update."""
        data = self.coordinator.data
        messages = data.get("messages", [])
        important = [
            m
            for m in messages
            if m.get("message", {}).get("importanceLevel") == "important"
        ]
        self._attr_native_value = len(important) if important else len(messages)
        self._attr_extra_state_attributes = {
            "messages": messages,
            "important_count": len(important),
        }
        self.async_write_ha_state()


class TisseoJourneySensor(CoordinatorEntity[TisseoInfoCoordinator], SensorEntity):
    """Sensor for journey duration."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:map-marker-path"
    _attr_native_unit_of_measurement = "min"
    _attr_translation_key = "journey"

    def __init__(
        self,
        coordinator: TisseoInfoCoordinator,
        entry: ConfigEntry,
        journey: dict,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._journey = journey
        self._attr_unique_id = (
            f"{entry.entry_id}_journey_"
            f"{journey[CONF_JOURNEY_ORIGIN]}_{journey[CONF_JOURNEY_DESTINATION]}"
        )
        self._attr_name = (
            f"Itinéraire {journey[CONF_JOURNEY_ORIGIN]} → "
            f"{journey[CONF_JOURNEY_DESTINATION]}"
        )
        self._attr_device_info = coordinator.device_info

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle update."""
        data = self.coordinator.data
        journey_data = data.get("journey")
        if not journey_data:
            self._attr_native_value = None
            self._attr_extra_state_attributes = {}
            self.async_write_ha_state()
            return

        journeys = journey_data.get("journeys", [])
        if journeys:
            first = journeys[0].get("journey", {})
            duration_str = first.get("duration", "00:00:00")
            try:
                parts = duration_str.split(":")
                minutes = int(parts[0]) * 60 + int(parts[1])
                self._attr_native_value = minutes
            except (ValueError, IndexError):
                self._attr_native_value = None

            self._attr_extra_state_attributes = {
                "departure": first.get("departureDateTime"),
                "arrival": first.get("arrivalDateTime"),
                "co2_emissions": first.get("co2_emissions"),
                "raw": first,
            }
        else:
            self._attr_native_value = None
            self._attr_extra_state_attributes = {}

        self.async_write_ha_state()
