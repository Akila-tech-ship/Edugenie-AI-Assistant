import unittest

from fastapi.testclient import TestClient

from main import app


class AppRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_homepage_renders(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])

    def test_health_route_reports_configuration(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertIn(response.json()["status"], {"healthy", "configuration_required"})

    def test_empty_question_returns_helpful_validation_error(self):
        response = self.client.post("/qa", json={"text": " "})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Please enter a question.")


if __name__ == "__main__":
    unittest.main()