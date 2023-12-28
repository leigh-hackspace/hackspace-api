import logging
from typing import Iterable, Optional
from urllib.parse import urljoin

import requests
from cachetools.func import ttl_cache
from prometheus_client import Summary

from hackspaceapi.config import settings
from hackspaceapi.services.session import get_requests_session

session = get_requests_session()
session.headers.update(
    {
        "Authorization": "Bearer {0}".format(settings.homeassistant_token),
        "content-type": "application/json",
    }
)

call_homeassistant_metrics = Summary(
    "hackspaceapi_homeassistant_api_time", "Summary of calls to the Home Assistant API"
)


@ttl_cache(ttl=60)
@call_homeassistant_metrics.time()
def call_homeassistant(endpoint: str, **params) -> Optional[Iterable]:
    """
    Call a Home Assistant API endpoint and return the JSON if successful
    """
    url = urljoin(settings.homeassistant_instance, endpoint)
    try:
        resp = session.get(url, params=params)
        if resp.ok:
            return resp.json()
    except requests.exceptions.RequestException as exc:
        logging.error("Failed to call {0} - {1}: {2}".format(url, endpoint, exc))
        pass
    return None


def get_entity_state(entity_id: str) -> Optional[Iterable]:
    """
    Call the configured Home Assistant API and retrieve the current state of a entity
    """
    return call_homeassistant("/api/states/{0}".format(entity_id))
