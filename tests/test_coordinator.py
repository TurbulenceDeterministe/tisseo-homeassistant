"""Verify API failures retain their endpoint through the initial data refresh."""
import importlib
import sys
import unittest
from types import ModuleType
from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp

from helpers import PACKAGE, api


class CoordinatorDouble:
    def __class_getitem__(cls, item):
        return cls


class UpdateFailed(Exception):
    pass


def load_coordinator():
    modules = {name: ModuleType(name) for name in (
        "homeassistant", "homeassistant.config_entries", "homeassistant.core",
        "homeassistant.helpers", "homeassistant.helpers.device_registry",
        "homeassistant.helpers.update_coordinator",
    )}
    modules["homeassistant.config_entries"].ConfigEntry = object
    modules["homeassistant.core"].HomeAssistant = object
    modules["homeassistant.helpers.device_registry"].DeviceInfo = dict
    modules["homeassistant.helpers.update_coordinator"].DataUpdateCoordinator = CoordinatorDouble
    modules["homeassistant.helpers.update_coordinator"].UpdateFailed = UpdateFailed
    with patch.dict(sys.modules, modules):
        return importlib.import_module(f"{PACKAGE}.coordinator")


coordinator_module = load_coordinator()


class FirstRefreshErrorTests(unittest.IsolatedAsyncioTestCase):
    def make_client(self, successful_payloads):
        responses = []
        for payload in [*successful_payloads, None]:
            response = MagicMock()
            response.__aenter__ = AsyncMock(return_value=response)
            response.__aexit__ = AsyncMock(return_value=False)
            response.json = AsyncMock(return_value=payload)
            response.status = 200 if payload is not None else 400
            if payload is None:
                response.raise_for_status.side_effect = aiohttp.ClientResponseError(
                    MagicMock(), (), status=400, message="secret-key"
                )
            responses.append(response)
        session = MagicMock()
        session.get.side_effect = responses
        return api.TisseoClient("secret-key", session)

    async def test_schedule_error_identifies_endpoint_in_setup_message(self):
        coordinator = object.__new__(coordinator_module.TisseoScheduleCoordinator)
        coordinator.client = self.make_client([])
        coordinator.stops = [{"stop_id": "stop_area:SA_206"}]
        with self.assertLogs(api._LOGGER, level="WARNING"):
            with self.assertRaisesRegex(
                UpdateFailed, "^API error: stops_schedules: HTTP 400$"
            ):
                await coordinator._async_update_data()

    async def test_each_information_endpoint_is_distinguishable(self):
        cases = [
            ([], "lines"),
            ([{"lines": {"line": []}}], "messages"),
            ([{"lines": {"line": []}}, {"messages": []}], "journeys"),
        ]
        for payloads, endpoint in cases:
            with self.subTest(endpoint=endpoint):
                coordinator = object.__new__(coordinator_module.TisseoInfoCoordinator)
                coordinator.client = self.make_client(payloads)
                coordinator.journey = {
                    "journey_origin": "Esquirol", "journey_destination": "Basso Cambo"
                }
                with self.assertLogs(api._LOGGER, level="WARNING"):
                    with self.assertRaisesRegex(
                        UpdateFailed, f"^API error: {endpoint}: HTTP 400$"
                    ):
                        await coordinator._async_update_data()


if __name__ == "__main__":
    unittest.main()
