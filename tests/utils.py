from fastapi.testclient import TestClient
from vcr.unittest import VCRTestCase

from hackspaceapi.main import app
from hackspaceapi.services.homeassistant import call_homeassistant
from hackspaceapi.services.prometheus import get_prometheus_metric

client = TestClient(app)


class FastAPIVCRTestCase(VCRTestCase):
    """
    A VCRTestCase modified to work nicely with FastAPI
    """

    cassette_name = None

    def _get_vcr(self, **kwargs):
        myvcr = super(FastAPIVCRTestCase, self)._get_vcr(**kwargs)
        myvcr.ignore_localhost = True
        myvcr.ignore_hosts = ["testserver"]
        myvcr.filter_headers = ["Authorization"]
        myvcr.filter_query_parameters = ["start", "end"]
        myvcr.match_on = ["method", "scheme", "port", "path", "query"]
        return myvcr

    def _get_cassette_name(self):
        if self.cassette_name:
            return self.cassette_name
        else:
            return f"{self.__class__.__name__}.{self._testMethodName}.yaml"

    def tearDown(self):
        super().tearDown()
        call_homeassistant.cache_clear()
        get_prometheus_metric.cache_clear()