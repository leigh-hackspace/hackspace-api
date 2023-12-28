from hackspaceapi import VERSION
from tests.utils import FastAPIVCRTestCase, client


class HealthTestCase(FastAPIVCRTestCase):
    """
    Test the health endpoint
    """

    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

        data = response.json()

        assert data["health"] == "ok"
        assert data["version"] == VERSION
