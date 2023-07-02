from typing import Dict, Optional
from urllib.parse import urljoin

import requests
from cachetools.func import ttl_cache

from hackspaceapi.config import settings


@ttl_cache(ttl=60)
def get_prometheus_metric(query: str) -> Optional[Dict]:
    resp = requests.get(
        urljoin(settings.prometheus_instance, "/api/v1/query"), params={"query": query}
    )
    if resp.ok:
        data = resp.json()
        if "status" in data and data["status"] == "success":
            return data["data"]
