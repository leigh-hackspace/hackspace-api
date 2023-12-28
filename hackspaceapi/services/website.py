import logging
from typing import Iterable, Optional

import requests
from cachetools.func import ttl_cache
from prometheus_client import Summary

from hackspaceapi.services.session import get_requests_session

session = get_requests_session()

website_metric_summary = Summary(
    "hackspaceapi_website_data_time", "Summary of calls to the Website data"
)


@ttl_cache(ttl=1800)
@website_metric_summary.time()
def get_membership_data() -> Optional[Iterable]:
    """
    Pull the JSON formatted membership plan data from the Leigh Hackspace
    website.
    """
    url = "https://web-test.leighhack.org/membership/index.json"
    try:
        resp = session.get(url)
        if resp.ok:
            data = resp.json()
            return data["memberships"]
    except requests.exceptions.RequestException as exc:
        logging.error("Failed query Website data - {0}: {1}".format(url, exc))
        pass
    return None
