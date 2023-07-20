from hackspaceapi.tests.utils import FastAPIVCRTestCase, client
from spacedirectory.models.space import Space


class SpaceAPINoNetworkTestCase(FastAPIVCRTestCase):
    """
    Test the SpaceAPI when we've got no on-going network to the backend systems
    """

    vcr_enabled = False

    def test_space_json_no_network(self):
        response = client.get("/space.json")
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

        data = response.json()

        # Check we provide a valid SpaceAPI JSON
        assert type(Space(data)) == Space

        # We should have no sensors
        assert len(data["sensors"]) == 0

        # Our status should be closed
        assert data["state"]["open"] is False

        # Last change shouldn't be in the state
        assert "lastchange" not in data["state"]


class SpaceAPITestCase(FastAPIVCRTestCase):
    """
    Test the SpaceAPI with recorded backend interactions
    """

    cassette_name = "SpaceAPITestCase.backend_calls.yaml"

    def test_space_json(self):
        response = client.get("/space.json")
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

        data = response.json()

        # Check we provide a valid SpaceAPI JSON
        assert type(Space(data)) == Space
