"""Tisséo integration for Home Assistant."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api_client import TisseoAPIError, TisseoAuthError, TisseoClient
from .const import (
    ATTR_ARRIVAL,
    ATTR_DATETIME,
    ATTR_DEPARTURE,
    CONF_API_KEY,
    CONF_JOURNEY,
    CONF_JOURNEY_DESTINATION,
    CONF_JOURNEY_ORIGIN,
    CONF_LINE_ID,
    CONF_LINES,
    CONF_STOPS,
    DOMAIN,
    SERVICE_CALCULATE_JOURNEY,
)
from .coordinator import TisseoInfoCoordinator, TisseoScheduleCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]

_LOGGER = logging.getLogger(__name__)

SERVICE_CALCULATE_JOURNEY_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_DEPARTURE): str,
        vol.Required(ATTR_ARRIVAL): str,
        vol.Optional(ATTR_DATETIME): str,
    }
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Tisséo from a config entry."""
    api_key = entry.data[CONF_API_KEY]
    session = async_get_clientsession(hass)
    client = TisseoClient(api_key, session)

    stops = entry.data.get(CONF_STOPS, [])
    lines = entry.data.get(CONF_LINES, [])
    journey = entry.data.get(CONF_JOURNEY)

    schedule_coordinator = TisseoScheduleCoordinator(hass, entry, client, stops)
    info_coordinator = TisseoInfoCoordinator(
        hass,
        entry,
        client,
        [l[CONF_LINE_ID] for l in lines],
        journey,
    )

    await schedule_coordinator.async_config_entry_first_refresh()
    await info_coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "schedule_coordinator": schedule_coordinator,
        "info_coordinator": info_coordinator,
        "stops": stops,
        "lines": lines,
        "journey": journey,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def async_handle_calculate_journey(call: ServiceCall) -> None:
        """Handle the calculate journey service call."""
        domain_data = hass.data.get(DOMAIN, {})
        if not domain_data:
            raise HomeAssistantError("No Tisséo integration configured")

        entry_id = list(domain_data.keys())[0]
        svc_client: TisseoClient = domain_data[entry_id]["client"]

        try:
            result = await svc_client.get_journeys(
                departure_place=call.data[ATTR_DEPARTURE],
                arrival_place=call.data[ATTR_ARRIVAL],
                first_departure_datetime=call.data.get(ATTR_DATETIME),
                number=3,
                display_wording=True,
            )
        except TisseoAuthError as err:
            raise HomeAssistantError(f"Authentication failed: {err}") from err
        except TisseoAPIError as err:
            raise HomeAssistantError(f"API error: {err}") from err

        hass.bus.fire(
            "tisseo_journey_result",
            {
                "departure": call.data[ATTR_DEPARTURE],
                "arrival": call.data[ATTR_ARRIVAL],
                "result": result,
            },
        )

    if not hass.services.has_service(DOMAIN, SERVICE_CALCULATE_JOURNEY):
        hass.services.async_register(
            DOMAIN,
            SERVICE_CALCULATE_JOURNEY,
            async_handle_calculate_journey,
            schema=SERVICE_CALCULATE_JOURNEY_SCHEMA,
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        if not hass.data[DOMAIN]:
            hass.services.async_remove(DOMAIN, SERVICE_CALCULATE_JOURNEY)
            hass.data.pop(DOMAIN)
    return unload_ok
