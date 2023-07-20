from hackspaceapi.tests.utils import FastAPIVCRTestCase, client
from ics import Calendar, Geo
from hackspaceapi.config import settings


class EventsTestCase(FastAPIVCRTestCase):

    cassette_name = "EventsTestCase.homeassistant_calendar.yaml"

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

    def test_valid_ics_event_contents(self):
        response = client.get("/events.ics")
        cal = Calendar(response.text)
        
        assert len(cal.events) > 1

        for event in cal.events:
            # Check if we have a Geo ref for the event
            assert type(event.geo) == Geo
            assert event.geo.latitude == settings.hackspace_address_lat
            assert event.geo.longitude == settings.hackspace_address_lon

            # Check the address field is defined and contains our address
            assert event.location == settings.hackspace_address
