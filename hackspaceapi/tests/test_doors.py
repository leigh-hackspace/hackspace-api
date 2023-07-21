from hackspaceapi.tests.utils import FastAPIVCRTestCase, client

VALID_DOOR_TAG = "12-34-AB-CD"
VALID_DOOR_TAG_NAME = "Test User"
INVALID_DOOR_TAG = "ObviousInvalidTag"


class DoorsAuthTestCase(FastAPIVCRTestCase):

    cassette_name = "DoorsAuthTestCase.authentik_calls.yaml"

    def test_successful_tag_read(self):
        response = client.post(
            "/doors/auth", json={"door_id": "unit-test-door", "uid": VALID_DOOR_TAG}
        )
        assert response.status_code == 200
        assert "name" in response.json()
        assert response.json()["name"] == VALID_DOOR_TAG_NAME

    def test_failed_tag_read(self):
        response = client.post(
            "/doors/auth",
            json={"door_id": "unit-test-door", "uid": INVALID_DOOR_TAG},
        )
        assert response.status_code == 403
        assert response.json()["fail"] is True
        assert response.json()["error"] == "No user found for UID"

    def test_invalid_auth_request(self):
        response = client.get("/doors/auth")
        assert response.status_code == 405

        response = client.post("/doors/auth", json={"door_id": "x"})
        assert response.status_code == 422

        response = client.post("/doors/auth", json={"uid": "x"})
        assert response.status_code == 422

    def test_valid_groups_auth(self):
        response = client.post(
            "/doors/auth",
            json={
                "door_id": "unit-test-door",
                "uid": VALID_DOOR_TAG,
                "groups": ["Public"],
            },
        )
        assert response.status_code == 200
        assert response.json()["fail"] is False
        assert response.json()["name"] == VALID_DOOR_TAG_NAME

    def test_invalid_groups_auth(self):
        response = client.post(
            "/doors/auth",
            json={
                "door_id": "unit-test-door",
                "uid": VALID_DOOR_TAG,
                "groups": ["LlamaFarmers"],
            },
        )
        assert response.status_code == 403
        assert response.json()["fail"] is True
        assert response.json()["error"] == "User is not a member of ['LlamaFarmers']"
