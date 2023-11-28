import logging

import requests
from cachetools.func import ttl_cache
from prometheus_client import Summary

from hackspaceapi.config import settings

website_metric_summary = Summary(
    "hackspaceapi_website_data_time", "Summary of calls to the Website data"
)


@ttl_cache(ttl=1800)
@website_metric_summary.time()
def get_membership_data() -> list:
    url = "https://web-test.leighhack.org/membership/index.json"
    try:
        resp = requests.get(url)
        if resp.ok:
            data = resp.json()
            return data["memberships"]
    except requests.exceptions.RequestException as exc:
        logging.error("Failed query Website data - {0}: {1}".format(url, exc))
        pass
    return []
