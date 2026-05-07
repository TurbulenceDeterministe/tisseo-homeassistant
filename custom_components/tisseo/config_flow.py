"""Config flow for Tisséo integration."""
from __future__ import annotations

import hashlib
import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_API_KEY
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TextSelectorType,
)

from .api_client import TisseoAPIError, TisseoAuthError, TisseoClient
from .const import (
    CONF_JOURNEY_DESTINATION,
    CONF_JOURNEY_ORIGIN,
    CONF_LINES,
    CONF_LINE_ID,
    CONF_LINE_NAME,
    CONF_LINE_SHORT_NAME,
    CONF_STOPS,
    CONF_STOP_ID,
    CONF_STOP_NAME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class TisseoConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tisséo."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize."""
        self._api_key: str | None = None
        self._client: TisseoClient | None = None
        self._stops: list[dict] = []
        self._lines: list[dict] = []
        self._search_results: list[dict] = []
        self._all_lines: list[dict] = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            api_key = user_input[CONF_API_KEY]
            session = async_get_clientsession(self.hass)
            client = TisseoClient(api_key, session)
            try:
                await client.get_networks()
            except TisseoAuthError:
                errors["base"] = "invalid_auth"
            except TisseoAPIError:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                self._api_key = api_key
                self._client = client
                unique_id = hashlib.sha256(api_key.encode()).hexdigest()
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()
                return await self.async_step_stops()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.PASSWORD)
                    ),
                }
            ),
            errors=errors,
        )

    async def async_step_stops(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle stop selection."""
        errors: dict[str, str] = {}
        if user_input is not None:
            if user_input.get("done"):
                if self._stops:
                    return await self.async_step_lines()
                errors["base"] = "no_stops_selected"
            else:
                search_term = user_input.get("search_term", "").strip()
                if len(search_term) >= 3:
                    try:
                        places = await self._client.get_places(
                            term=search_term,
                            number=10,
                            display_only_stop_areas=True,
                        )
                    except TisseoAPIError:
                        errors["base"] = "cannot_connect"
                    else:
                        options = []
                        for place in places.get("places", []):
                            stop = place.get("stopArea", {})
                            if stop:
                                options.append(
                                    {
                                        "label": f"{stop.get('name')} ({stop.get('cityName', 'N/A')})",
                                        "value": stop.get("id"),
                                    }
                                )
                        if options:
                            self._search_results = options
                            return await self.async_step_pick_stop()
                        errors["base"] = "no_results"
                else:
                    errors["base"] = "search_too_short"

        return self.async_show_form(
            step_id="stops",
            data_schema=vol.Schema(
                {
                    vol.Optional("search_term", default=""): str,
                    vol.Optional("done", default=False): bool,
                }
            ),
            errors=errors,
            description_placeholders={
                "selected_stops": ", ".join(
                    s[CONF_STOP_NAME] for s in self._stops
                )
                or "Aucun"
            },
        )

    async def async_step_pick_stop(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Pick a stop from search results."""
        if user_input is not None:
            selected_id = user_input["stop_id"]
            selected_label = next(
                (
                    o["label"]
                    for o in self._search_results
                    if o["value"] == selected_id
                ),
                selected_id,
            )
            self._stops.append(
                {
                    CONF_STOP_ID: selected_id,
                    CONF_STOP_NAME: selected_label.split(" (")[0],
                }
            )
            return await self.async_step_stops()

        options = self._search_results
        return self.async_show_form(
            step_id="pick_stop",
            data_schema=vol.Schema(
                {
                    vol.Required("stop_id"): SelectSelector(
                        SelectSelectorConfig(
                            options=[
                                {"label": o["label"], "value": o["value"]}
                                for o in options
                            ],
                            mode=SelectSelectorMode.LIST,
                        )
                    ),
                }
            ),
        )

    async def async_step_lines(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle line selection."""
        if user_input is not None:
            selected = user_input.get("lines", [])
            self._lines = [
                {
                    CONF_LINE_ID: line_id,
                    CONF_LINE_SHORT_NAME: next(
                        (
                            l["shortName"]
                            for l in self._all_lines
                            if l["id"] == line_id
                        ),
                        line_id,
                    ),
                    CONF_LINE_NAME: next(
                        (
                            l["name"]
                            for l in self._all_lines
                            if l["id"] == line_id
                        ),
                        line_id,
                    ),
                }
                for line_id in selected
            ]
            return await self.async_step_journey()

        try:
            lines_data = await self._client.get_lines()
            raw_lines = lines_data.get("lines", {}).get("line", [])
            if isinstance(raw_lines, dict):
                self._all_lines = [raw_lines]
            else:
                self._all_lines = raw_lines
        except TisseoAPIError:
            self._all_lines = []

        options = [
            {"label": f"{line['shortName']} - {line['name']}", "value": line["id"]}
            for line in self._all_lines
        ]

        return self.async_show_form(
            step_id="lines",
            data_schema=vol.Schema(
                {
                    vol.Optional("lines", default=[]): SelectSelector(
                        SelectSelectorConfig(
                            options=options,
                            mode=SelectSelectorMode.DROPDOWN,
                            multiple=True,
                        )
                    ),
                }
            ),
        )

    async def async_step_journey(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle optional journey configuration."""
        if user_input is not None:
            origin = user_input.get(CONF_JOURNEY_ORIGIN, "").strip()
            destination = user_input.get(CONF_JOURNEY_DESTINATION, "").strip()
            journey = None
            if origin and destination:
                journey = {
                    CONF_JOURNEY_ORIGIN: origin,
                    CONF_JOURNEY_DESTINATION: destination,
                }
            return self.async_create_entry(
                title="Tisséo",
                data={
                    CONF_API_KEY: self._api_key,
                    CONF_STOPS: self._stops,
                    CONF_LINES: self._lines,
                    CONF_JOURNEY: journey,
                },
            )

        return self.async_show_form(
            step_id="journey",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_JOURNEY_ORIGIN, default=""): str,
                    vol.Optional(CONF_JOURNEY_DESTINATION, default=""): str,
                }
            ),
            description_placeholders={
                "info": "Laissez vide pour ne pas configurer d'itinéraire."
            },
        )
