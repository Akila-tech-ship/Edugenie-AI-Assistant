import unittest
from types import SimpleNamespace

from gemini_utils import generate_with_fallback, get_model_candidates


class GenerateWithFallbackTests(unittest.TestCase):
    def test_model_candidates_include_supported_default_names(self):
        models = get_model_candidates("gemini-3.8-flash")
        self.assertIn("gemini-3.8-flash", models)
        self.assertIn("gemini-3.5-flash", models)

    def test_model_candidates_use_api_supported_names_first(self):
        models = get_model_candidates(
            "gemini-3.8-flash",
            ["gemini-3.5-flash", "gemini-2.5-flash-lite"],
        )
        self.assertEqual(models[0], "gemini-3.8-flash")
        self.assertIn("gemini-3.5-flash", models)
        self.assertIn("gemini-2.5-flash-lite", models)
        self.assertEqual(models.count("gemini-3.5-flash"), 1)

    def test_retries_with_next_model_after_service_unavailable(self):
        class ApiError(Exception):
            code = 503

        calls = []

        def generate_content(**kwargs):
            calls.append(kwargs["model"])
            if len(calls) == 1:
                raise ApiError("service unavailable")
            return "generated response"

        client = SimpleNamespace(
            models=SimpleNamespace(generate_content=generate_content)
        )

        response = generate_with_fallback(client, "prompt", "gemini-3.8-flash")

        self.assertEqual(response, "generated response")
        self.assertEqual(calls, ["gemini-3.8-flash", "gemini-3.5-flash-lite"])

    def test_does_not_retry_authentication_errors(self):
        class ApiError(Exception):
            code = 401

        calls = []

        def generate_content(**kwargs):
            calls.append(kwargs["model"])
            raise ApiError("unauthorized")

        client = SimpleNamespace(
            models=SimpleNamespace(generate_content=generate_content)
        )

        with self.assertRaises(ApiError):
            generate_with_fallback(client, "prompt", "gemini-3.8-flash")

        self.assertEqual(calls, ["gemini-3.8-flash"])
