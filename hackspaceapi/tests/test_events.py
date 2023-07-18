from fastapi.testclient import TestClient
from unittest import TestCase
from ics import Calendar

from hackspaceapi.main import app

client = TestClient(app)


class EventsTestCase(TestCase):
    def test_events_json(self):
        response = client.get("/events/")
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

    def test_events_ics(self):
        response = client.get("/events.ics")
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "text/calendar; charset=utf-8"

    def test_events_ics_specific_calendar(self):
        response = client.get("/events.ics?calendar=public")
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "text/calendar; charset=utf-8"

    def test_events_ics_incorrect_calendar(self):
        response = client.get("/events.ics?calendar=llama")
        assert response.status_code == 422

    def test_invalid_events_request(self):
        response = client.post("/events/")
        assert response.status_code == 405

        response = client.post("/events.ics")
        assert response.status_code == 405

    def test_valid_ics_response(self):
        response = client.get("/events.ics")
        cal = Calendar(response.text)
        assert len(cal.events) > 1
