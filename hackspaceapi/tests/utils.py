from fastapi.testclient import TestClient
from vcr.unittest import VCRTestCase
from hackspaceapi.main import app


client = TestClient(app)


class FastAPIVCRTestCase(VCRTestCase):
    """
    A VCRTestCase modified to work nicely with FastAPI
    """

    def _get_vcr(self, **kwargs):
        myvcr = super(FastAPIVCRTestCase, self)._get_vcr(**kwargs)
        myvcr.ignore_localhost = True
        myvcr.ignore_hosts = ["testserver"]
        myvcr.filter_headers = ["Authorization"]
        myvcr.filter_query_parameters = ["start", "end"]
        myvcr.match_on = ["method", "scheme", "port", "path", "query"]
        return myvcr
