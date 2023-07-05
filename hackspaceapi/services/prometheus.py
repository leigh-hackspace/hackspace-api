import logging
from typing import Dict, Optional
from urllib.parse import urljoin

import requests
from cachetools.func import ttl_cache
from prometheus_client import Summary

from hackspaceapi.config import settings

prometheus_metric_summary = Summary('hackspaceapi_prometheus_api_time', 'Summary of calls to the Prometheus API')

@ttl_cache(ttl=60)
@prometheus_metric_summary.time()
def get_prometheus_metric(query: str) -> Optional[Dict]:
    url = urljoin(settings.prometheus_instance, "/api/v1/query")
    try:
        resp = requests.get(url, params={"query": query})
        if resp.ok:
            data = resp.json()
            if "status" in data and data["status"] == "success":
                return data["data"]
    except requests.exceptions.RequestException as exc:
        logging.error("Failed query Prometheus - {1}".format(url), exc)
        pass
    return None
