from hackspaceapi.services.homeassistant import get_entity_state
from hackspaceapi.services.prometheus import get_prometheus_metric
from hackspaceapi.services.website import get_membership_data
from tests.utils import FastAPIVCRTestCase


class ServicesHomeassistantTestCase(FastAPIVCRTestCase):
    def test_simple_call(self):
        ENTITY = "weather.forecast_leigh_hackspace"

        resp = get_entity_state(ENTITY)

        assert resp["entity_id"] == ENTITY

    def test_simple_invalid_call(self):
        ENTITY = "nope.nope"

        resp = get_entity_state(ENTITY)

        assert resp == None


class ServicesPrometheusTestCase(FastAPIVCRTestCase):
    def test_simple_call(self):
        QUERY = "gocardless_members_count{}"

        resp = get_prometheus_metric(QUERY)

        assert isinstance(resp, dict)
        assert len(resp["result"])

    def test_simple_invalid_call(self):
        QUERY = "gocardless_members_cxxount{}"

        resp = get_prometheus_metric(QUERY)

        assert isinstance(resp, dict)
        assert len(resp["result"]) == 0


class ServicesWebsiteTestCase(FastAPIVCRTestCase):
    def test_simple_call(self):
        resp = get_membership_data()

        assert isinstance(resp, list)
