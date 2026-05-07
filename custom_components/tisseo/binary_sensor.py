"""Binary sensor platform for Tisséo."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_LINE_ID, CONF_LINE_NAME, CONF_LINE_SHORT_NAME, DOMAIN
from .coordinator import TisseoInfoCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary sensors."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: TisseoInfoCoordinator = data["info_coordinator"]
    lines = data["lines"]

    entities: list[BinarySensorEntity] = []
    for line in lines:
        entities.append(TisseoLineDisruptionSensor(coordinator, line, entry))

    async_add_entities(entities)


class TisseoLineDisruptionSensor(
    CoordinatorEntity[TisseoInfoCoordinator], BinarySensorEntity
):
    """Binary sensor for line disruption."""

    _attr_has_entity_name = True
    _attr_device_class = None

    def __init__(
        self,
        coordinator: TisseoInfoCoordinator,
        line: dict,
        entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._line_id = line[CONF_LINE_ID]
        self._line_short_name = line[CONF_LINE_SHORT_NAME]
        self._line_name = line.get(CONF_LINE_NAME, self._line_short_name)
        self._attr_unique_id = f"{entry.entry_id}_line_disruption_{self._line_id}"
        self._attr_name = f"Perturbation ligne {self._line_short_name}"
        self._attr_device_info = coordinator.device_info

    @property
    def icon(self) -> str:
        """Return the icon."""
        return "mdi:bus-alert" if self.is_on else "mdi:bus"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle update."""
        lines = self.coordinator.data.get("lines", {})
        line_data = lines.get(self._line_id, {})
        messages = line_data.get("messages", [])
        self._attr_is_on = bool(messages)
        self._attr_extra_state_attributes = {
            "messages": messages,
            "line_name": self._line_name,
            "line_id": self._line_id,
        }
        self.async_write_ha_state()
