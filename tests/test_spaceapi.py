import requests
from spacedirectory.models.space import Space

from tests.utils import FastAPIVCRTestCase, client


def validate_spacejson_schema(data):
    """
    Call the SpaceAPI validator service
    """
    resp = requests.post(
        "https://validator.spaceapi.io/v2/validateJSON",
        headers={"Content-Type": "application/json"},
        json=data,
    )

    assert resp.ok
    rdata = resp.json()

    # If we have schema errors, print them so they'll be visible when the test fails
    if "schemaErrors" in rdata and len(rdata["schemaErrors"]):
        for err in rdata["schemaErrors"]:
            print(err)
    assert rdata["valid"] is True


class SpaceAPINoNetworkTestCase(FastAPIVCRTestCase):
    """
    Test the SpaceAPI when we've got no on-going network to the backend systems
    """

    vcr_enabled = False

    def setUp(self):
        # Disable the service functions (covered by separate tests)
        # Use the 'imported path' rather than the module path, see: https://nedbatchelder.com/blog/201908/why_your_mock_doesnt_work.html#h_mock_it_where_its_used
        self.mocker.patch("hackspaceapi.spaceapi.get_entity_state", return_value=None)
        self.mocker.patch("hackspaceapi.spaceapi.get_prometheus_metric", return_value=None)
        self.mocker.patch("hackspaceapi.spaceapi.get_membership_data", return_value=[])

    def test_space_json_no_network(self):
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

    def test_validate_space_json_no_network(self):
        data = client.get("/space.json").json()
        validate_spacejson_schema(data)


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

    def test_validate_space_json(self):
        data = client.get("/space.json").json()
        validate_spacejson_schema(data)
