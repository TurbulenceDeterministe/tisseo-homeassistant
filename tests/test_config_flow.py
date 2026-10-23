"""Exercise flow transitions with lightweight Home Assistant framework doubles.

These tests run the integration's actual client and flow methods; Home Assistant's
form rendering and config-entry registry are outside their scope.
"""
import importlib
import sys
import unittest
from types import ModuleType
from unittest.mock import AsyncMock, MagicMock, patch

from helpers import PACKAGE, api
from test_api_client import STOP


class ConfigFlowDouble:
    def __init_subclass__(cls, *, domain=None, **kwargs):
        super().__init_subclass__(**kwargs)

    def async_show_form(self, **kwargs):
        return {"type": "form", **kwargs}

    def async_create_entry(self, **kwargs):
        return {"type": "create_entry", **kwargs}

    async def async_set_unique_id(self, unique_id):
        self.unique_id = unique_id

    def _abort_if_unique_id_configured(self):
        pass


def load_flow():
    modules = {name: ModuleType(name) for name in (
        "homeassistant", "homeassistant.config_entries", "homeassistant.const",
        "homeassistant.core", "homeassistant.helpers",
        "homeassistant.helpers.aiohttp_client",
    )}
    modules["homeassistant.config_entries"].ConfigFlow = ConfigFlowDouble
    modules["homeassistant.const"].CONF_API_KEY = "api_key"
    modules["homeassistant.core"].callback = lambda method: method
    modules["homeassistant.helpers.aiohttp_client"].async_get_clientsession = (
        lambda hass: MagicMock()
    )
    with patch.dict(sys.modules, modules):
        return importlib.import_module(f"{PACKAGE}.config_flow")


flow_module = load_flow()


class ConfigFlowTests(unittest.IsolatedAsyncioTestCase):
    async def test_onboarding_from_key_to_saved_entry(self):
        flow = flow_module.TisseoConfigFlow()
        flow.hass = object()
        responses = [
            {"networks": [{"id": "network:1", "name": "Tisséo"}]},
            {"placesList": {"place": [STOP]}},
            {"lines": {"line": []}},
        ]
        with patch.object(api.TisseoClient, "_request", AsyncMock(side_effect=responses)):
            result = await flow.async_step_user({"api_key": " secret-key \n"})
            self.assertEqual(result["step_id"], "stops")
            result = await flow.async_step_stops({"search_term": " Basso "})
            self.assertEqual(result["step_id"], "pick_stop")
            self.assertEqual(flow._search_results, [{
                "label": "Basso Cambo (TOULOUSE)", "value": STOP["id"],
            }])
            await flow.async_step_pick_stop({"stop_id": STOP["id"]})
            result = await flow.async_step_stops({"done": True})
            self.assertEqual(result["step_id"], "lines")
            result = await flow.async_step_lines({"lines": ""})
            self.assertEqual(result["step_id"], "journey")
            result = await flow.async_step_journey({})
        self.assertEqual(result["type"], "create_entry")
        self.assertEqual(result["data"]["api_key"], "secret-key")
        self.assertEqual(result["data"]["stops"], [{
            "stop_id": STOP["id"], "stop_name": STOP["name"],
        }])
        self.assertIsNone(result["data"]["journey"])

    async def test_empty_results_stay_on_search_form(self):
        flow = flow_module.TisseoConfigFlow()
        flow._client = api.TisseoClient("secret-key", MagicMock())
        flow._client._request = AsyncMock(return_value={"places": []})
        result = await flow.async_step_stops({"search_term": "zzzzzz"})
        self.assertEqual(result["errors"], {"base": "no_results"})

    async def test_short_search_does_not_call_api(self):
        flow = flow_module.TisseoConfigFlow()
        flow._client = MagicMock()
        result = await flow.async_step_stops({"search_term": " ab "})
        self.assertEqual(result["errors"], {"base": "search_too_short"})
        flow._client.search_stop_areas.assert_not_called()

    async def test_auth_and_api_errors_remain_distinct(self):
        for error, expected in (
            (api.TisseoAuthError("Invalid API key"), "invalid_auth"),
            (api.TisseoAPIError("API request timed out"), "cannot_connect"),
        ):
            flow = flow_module.TisseoConfigFlow()
            flow._client = MagicMock()
            flow._client.search_stop_areas = AsyncMock(side_effect=error)
            with self.assertLogs(flow_module._LOGGER, level="WARNING"):
                result = await flow.async_step_stops({"search_term": "Basso"})
            self.assertEqual(result["errors"], {"base": expected})


if __name__ == "__main__":
    unittest.main()
