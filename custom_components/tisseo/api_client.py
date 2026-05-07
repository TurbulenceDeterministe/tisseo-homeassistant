"""API client for Tisséo Open Data API v2."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp

from .const import API_BASE_URL, DEFAULT_NETWORK, DEFAULT_TIMEOUT

_LOGGER = logging.getLogger(__name__)


class TisseoAPIError(Exception):
    """Generic API error."""


class TisseoAuthError(TisseoAPIError):
    """Authentication error."""


class TisseoClient:
    """Async client for Tisséo API v2."""

    def __init__(self, api_key: str, session: aiohttp.ClientSession) -> None:
        """Initialize."""
        self._api_key = api_key
        self._session = session

    async def _request(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make a GET request."""
        url = f"{API_BASE_URL}/{endpoint}.json"
        req_params: dict[str, Any] = {"key": self._api_key}
        if params:
            req_params.update(params)

        try:
            async with self._session.get(
                url, params=req_params, timeout=aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT)
            ) as resp:
                if resp.status in (401, 403):
                    raise TisseoAuthError("Invalid API key")
                resp.raise_for_status()
                try:
                    data = await resp.json()
                except aiohttp.ContentTypeError:
                    text = await resp.text()
                    if "No key provided" in text:
                        raise TisseoAuthError("No API key provided")
                    raise TisseoAPIError(f"Unexpected response: {text}")

                if isinstance(data, dict) and data.get("message") == "No key provided":
                    raise TisseoAuthError("No API key provided")
                return data
        except aiohttp.ClientResponseError as err:
            raise TisseoAPIError(f"HTTP {err.status}: {err.message}") from err
        except aiohttp.ClientError as err:
            raise TisseoAPIError(f"Connection error: {err}") from err

    async def get_networks(self) -> dict[str, Any]:
        """Get available networks."""
        return await self._request("networks")

    async def get_stop_areas(
        self,
        line_id: str | None = None,
        display_lines: bool = False,
        display_coord: bool = False,
    ) -> dict[str, Any]:
        """Get stop areas."""
        params: dict[str, Any] = {"network": DEFAULT_NETWORK}
        if line_id:
            params["lineId"] = line_id
        if display_lines:
            params["displayLines"] = 1
        if display_coord:
            params["displayCoordXY"] = 1
        return await self._request("stop_areas", params)

    async def get_stop_points(
        self,
        stop_area_id: str | None = None,
        line_id: str | None = None,
        display_lines: bool = False,
    ) -> dict[str, Any]:
        """Get stop points."""
        params: dict[str, Any] = {"network": DEFAULT_NETWORK}
        if stop_area_id:
            params["stopAreaId"] = stop_area_id
        if line_id:
            params["lineId"] = line_id
        if display_lines:
            params["displayLines"] = 1
        return await self._request("stop_points", params)

    async def get_places(
        self,
        term: str | None = None,
        coordinates_xy: str | None = None,
        number: int = 10,
        display_best_place: bool = False,
        display_only_stop_areas: bool = False,
    ) -> dict[str, Any]:
        """Search places."""
        params: dict[str, Any] = {"network": DEFAULT_NETWORK, "number": number}
        if term:
            params["term"] = term
        if coordinates_xy:
            params["coordinatesXY"] = coordinates_xy
        if display_best_place:
            params["displayBestPlace"] = 1
        if display_only_stop_areas:
            params["displayOnlyStopAreas"] = 1
        return await self._request("places", params)

    async def get_lines(
        self,
        line_id: str | None = None,
        short_name: str | None = None,
        display_messages: bool = False,
        display_only_disrupted: bool = False,
        display_terminus: bool = False,
    ) -> dict[str, Any]:
        """Get lines."""
        params: dict[str, Any] = {"network": DEFAULT_NETWORK}
        if line_id:
            params["lineId"] = line_id
        if short_name:
            params["shortName"] = short_name
        if display_messages:
            params["displayMessages"] = 1
        if display_only_disrupted:
            params["displayOnlyDisrupted"] = 1
        if display_terminus:
            params["displayTerminus"] = 1
        return await self._request("lines", params)

    async def get_stop_schedules(
        self,
        stop_area_id: str | None = None,
        stop_point_id: str | None = None,
        stops_list: str | None = None,
        line_id: str | None = None,
        number: int = 5,
        display_real_time: bool = True,
        timetable_by_area: bool = True,
    ) -> dict[str, Any]:
        """Get stop schedules."""
        params: dict[str, Any] = {
            "network": DEFAULT_NETWORK,
            "number": number,
            "timetableByArea": 1 if timetable_by_area else 0,
            "displayRealTime": 1 if display_real_time else 0,
        }
        if stop_area_id:
            params["stopAreaId"] = stop_area_id
        if stop_point_id:
            params["stopPointId"] = stop_point_id
        if stops_list:
            params["stopsList"] = stops_list
        if line_id:
            params["lineId"] = line_id
        return await self._request("stops_schedules", params)

    async def get_messages(
        self, display_important_only: bool = False, content_format: str = "text"
    ) -> dict[str, Any]:
        """Get network messages."""
        params: dict[str, Any] = {
            "network": DEFAULT_NETWORK,
            "contentFormat": content_format,
            "displayImportantOnly": 1 if display_important_only else 0,
        }
        return await self._request("messages", params)

    async def get_journeys(
        self,
        departure_place: str | None = None,
        arrival_place: str | None = None,
        departure_place_xy: str | None = None,
        arrival_place_xy: str | None = None,
        number: int = 3,
        first_departure_datetime: str | None = None,
        display_wording: bool = True,
        lang: str = "fr",
    ) -> dict[str, Any]:
        """Calculate journey."""
        params: dict[str, Any] = {
            "networkList": DEFAULT_NETWORK,
            "number": number,
            "displayWording": 1 if display_wording else 0,
            "lang": lang,
        }
        if departure_place:
            params["departurePlace"] = departure_place
        if arrival_place:
            params["arrivalPlace"] = arrival_place
        if departure_place_xy:
            params["departurePlaceXY"] = departure_place_xy
        if arrival_place_xy:
            params["arrivalPlaceXY"] = arrival_place_xy
        if first_departure_datetime:
            params["firstDepartureDatetime"] = first_departure_datetime
        return await self._request("journeys", params)

    async def get_rolling_stocks(self) -> dict[str, Any]:
        """Get rolling stocks (transport modes)."""
        return await self._request("rolling_stocks")
