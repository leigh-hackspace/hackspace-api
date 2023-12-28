from spacedirectory.models.space import Space

from tests.utils import FastAPIVCRTestCase, client


class SpaceAPINoNetworkTestCase(FastAPIVCRTestCase):
    """
    Test the SpaceAPI when we've got no on-going network to the backend systems
    """

    vcr_enabled = False

    def test_space_json_no_network(self):
        # Disable the service functions (covered by separate tests)
        # Use the 'imported path' rather than the module path, see: https://nedbatchelder.com/blog/201908/why_your_mock_doesnt_work.html#h_mock_it_where_its_used
        self.mocker.patch("hackspaceapi.spaceapi.get_entity_state", return_value=None)
        self.mocker.patch(
            "hackspaceapi.spaceapi.get_prometheus_metric", return_value=None
        )
        self.mocker.patch("hackspaceapi.spaceapi.get_membership_data", return_value=[])

        response = client.get("/space.json")
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        data = response.json()

        # Check we provide a valid SpaceAPI JSON
        assert type(Space(data)) == Space

        # We should have no sensors
        assert len(data["sensors"]) == 0

        # We should have no membership data
        assert len(data["membership_plans"]) == 0

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
