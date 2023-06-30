from typing import Iterable, Optional
from urllib.parse import urljoin

import requests
from cachetools.func import ttl_cache

from hackspaceapi.config import settings

session = requests.session()
session.headers = {
    "Authorization": "Bearer {0}".format(settings.homeassistant_token),
    "content-type": "application/json",
}


@ttl_cache(ttl=60)
def call_homeassistant(endpoint: str, **params) -> Optional[Iterable]:
    """
    Call a Homeassistant API endpoint and return the JSON if successful
    """
    resp = session.get(urljoin(settings.homeassistant_instance, endpoint), params=params)
    if resp.ok:
        return resp.json()


def get_entity_state(entity_id: str) -> Optional[Iterable]:
    return call_homeassistant("/api/states/{0}".format(entity_id))
