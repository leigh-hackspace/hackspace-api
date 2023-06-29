from typing import Dict, Optional
from urllib.parse import urljoin

import requests

from .config import settings


def get_prometheus_metric(query: str) -> Optional[Dict]:
    resp = requests.get(urljoin(settings.prometheus_instance, "/api/v1/query"), params={"query": query})
    if resp.ok:
        data = resp.json()
        if "status" in data and data["status"] == "success":
            return data["data"]
