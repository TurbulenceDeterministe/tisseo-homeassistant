"""Regression coverage for stop search payloads and safe API failures."""
import unittest
from unittest.mock import AsyncMock, MagicMock

import aiohttp

from helpers import api

STOP = {"id": "stop_area:SA_206", "name": "Basso Cambo", "cityName": "TOULOUSE"}


class StopSearchTests(unittest.IsolatedAsyncioTestCase):
    async def test_supported_envelopes_and_singletons(self):
        flat = {"id": STOP["id"], "label": STOP["name"], "type": "stop_area",
                "cityName": STOP["cityName"]}
        payloads = [
            {"placesList": {"place": [flat]}},
            {"placesList": {"place": flat}},
            {"places": [STOP]},
            {"places": {"place": [STOP]}},
            {"places": {"place": STOP}},
            {"places": [{"stopArea": STOP}]},
            {"places": {"stopArea": STOP}},
        ]
        for payload in payloads:
            with self.subTest(payload=payload):
                client = api.TisseoClient("secret", MagicMock())
                client._request = AsyncMock(return_value=payload)
                self.assertEqual(await client.search_stop_areas("Basso"), [STOP])
                client._request.assert_awaited_once_with("places", {
                    "network": "Tisséo", "number": 10, "term": "Basso",
                    "displayOnlyStopAreas": 1,
                })

    async def test_ignores_non_stops_invalid_items_and_duplicates(self):
        client = api.TisseoClient("secret", MagicMock())
        client._request = AsyncMock(return_value={"places": [
            STOP, STOP, None, "invalid", {}, {"stopArea": None},
            {"id": "road:1", "label": "Rue de Metz", "type": "road"},
            {"id": "stop_point:SP_1", "name": "Pole", "className": "stop"},
            {"id": "stop_area:SA_1"}, {"id": 42, "name": "Bad ID"},
        ]})
        self.assertEqual(await client.search_stop_areas("Basso"), [STOP])

    async def test_empty_search(self):
        for payload in ({"places": []}, {"placesList": {"place": []}}):
            client = api.TisseoClient("secret", MagicMock())
            client._request = AsyncMock(return_value=payload)
            self.assertEqual(await client.search_stop_areas("zzzzzz"), [])

    async def test_unknown_payload_is_not_reported_as_no_results(self):
        for payload in ({"error": "failed"}, {"places": "invalid"}):
            client = api.TisseoClient("secret", MagicMock())
            client._request = AsyncMock(return_value=payload)
            with self.assertRaises(api.TisseoAPIError):
                await client.search_stop_areas("Basso")

    async def test_debug_logs_do_not_expose_key_search_or_payload(self):
        client = api.TisseoClient("secret-key", MagicMock())
        client._request = AsyncMock(return_value={"places": [STOP]})
        with self.assertLogs(api._LOGGER, level="DEBUG") as logs:
            await client.search_stop_areas("private-search")
        output = "\n".join(logs.output)
        self.assertIn("1 entries and 1 usable stop areas", output)
        for sensitive in ("secret-key", "private-search", STOP["id"], STOP["name"]):
            self.assertNotIn(sensitive, output)


class RequestTests(unittest.IsolatedAsyncioTestCase):
    def make_client(self, status=200, payload=None):
        response = MagicMock()
        response.status = status
        response.json = AsyncMock(return_value=payload)
        response.text = AsyncMock(return_value="body containing secret-key")
        response.__aenter__ = AsyncMock(return_value=response)
        response.__aexit__ = AsyncMock(return_value=False)
        session = MagicMock()
        session.get.return_value = response
        return api.TisseoClient("secret-key", session), response

    async def test_success_uses_v2_without_logging_query_parameters(self):
        payload = {"networks": []}
        client, _ = self.make_client(payload=payload)
        with self.assertLogs(api._LOGGER, level="DEBUG") as logs:
            self.assertEqual(await client.get_networks(), payload)
        args, kwargs = client._session.get.call_args
        self.assertEqual(args, ("https://api.tisseo.fr/v2/networks.json",))
        self.assertEqual(kwargs["params"], {"key": "secret-key"})
        self.assertNotIn("secret-key", "\n".join(logs.output))

    async def test_timeout_and_connection_errors_are_sanitized(self):
        for failure in (TimeoutError(), aiohttp.ClientConnectionError("secret-key")):
            client, _ = self.make_client()
            client._session.get.side_effect = failure
            with self.assertRaises(api.TisseoAPIError) as raised:
                await client.get_networks()
            self.assertNotIn("secret-key", str(raised.exception))
            self.assertTrue(raised.exception.__suppress_context__)

    async def test_http_auth_errors(self):
        for status in (401, 403):
            client, _ = self.make_client(status)
            with self.assertRaises(api.TisseoAuthError):
                await client.get_networks()

    async def test_http_status_does_not_leak_response_url(self):
        client, response = self.make_client(500)
        response.raise_for_status.side_effect = aiohttp.ClientResponseError(
            MagicMock(), (), status=500, message="secret-key"
        )
        with self.assertRaisesRegex(api.TisseoAPIError, "^networks: HTTP 500$"):
            await client.get_networks()

    async def test_http_400_reports_endpoint_without_debug_logging(self):
        client, response = self.make_client(400)
        response.raise_for_status.side_effect = aiohttp.ClientResponseError(
            MagicMock(), (), status=400, message="secret-key"
        )
        with self.assertLogs(api._LOGGER, level="WARNING") as logs:
            with self.assertRaisesRegex(
                api.TisseoAPIError, "^stops_schedules: HTTP 400$"
            ):
                await client.get_stop_schedules(stop_area_id="stop_area:SA_206")
        self.assertIn("stops_schedules failed: HTTP 400", "\n".join(logs.output))
        for sensitive in ("secret-key", "stop_area:SA_206", "https://"):
            self.assertNotIn(sensitive, "\n".join(logs.output))

    async def test_invalid_json_and_content_types(self):
        for failure in (ValueError("secret-key"),
                        aiohttp.ContentTypeError(MagicMock(), (), message="secret-key")):
            client, response = self.make_client()
            response.json.side_effect = failure
            with self.assertRaises(api.TisseoAPIError) as raised:
                await client.get_networks()
            self.assertNotIn("secret-key", str(raised.exception))

    async def test_non_json_missing_key_is_auth_error(self):
        client, response = self.make_client()
        response.json.side_effect = aiohttp.ContentTypeError(MagicMock(), ())
        response.text.return_value = "No key provided"
        with self.assertRaises(api.TisseoAuthError):
            await client.get_networks()

    async def test_unexpected_json_shape(self):
        client, _ = self.make_client(payload=[])
        with self.assertRaises(api.TisseoAPIError):
            await client.get_networks()


if __name__ == "__main__":
    unittest.main()
