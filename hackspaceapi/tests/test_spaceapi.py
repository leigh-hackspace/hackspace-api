from hackspaceapi.tests.utils import FastAPIVCRTestCase, client
from spacedirectory.directory import get_space_from_data
from spacedirectory.space import Space


class SpaceAPITestCase(FastAPIVCRTestCase):
    def test_space_json(self):
        response = client.get("/space.json")
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

        # Check we provide a valid SpaceAPI JSON
        assert type(get_space_from_data(response.json())) == Space
