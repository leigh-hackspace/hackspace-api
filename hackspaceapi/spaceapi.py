# -*- coding: utf-8 -*-
from urllib.parse import urljoin
import arrow
import time

from cachetools.func import ttl_cache
from fastapi import APIRouter

from .config import settings
from .prometheus import get_prometheus_metric
from .homeassistant import get_entity_state

spaceapi = APIRouter()


SENSORS = (
    (
        "temperature",
        "Rack 1",
        "Average Temperature",
        "round(avg(homeassistant_sensor_temperature_celsius) + 273.15)",
        "K",
    ),
    (
        "network_connections",
        "Hackspace",
        "WiFi Devices",
        "sum(homeassistant_sensor_unit_clients{entity='sensor.gw_dhcp_leases_online'})",
        None,
    ),
)

def get_state():
    data = get_entity_state('input_boolean.hackspace_open')

    return {
        'open': data['state'] == 'on',
        'lastchange': arrow.get(data['last_changed']).timestamp(),
    }

@ttl_cache(ttl=60)
def get_sensors():
    result = {}
    for typ, location, name, query, unit in SENSORS:
        res = get_prometheus_metric(query)
        if not res:
            continue
        if typ not in result:
            result[typ] = []

        sensor_data = {
            "location": location,
            "name": name,
            "value": float(res["result"][0]["value"][1]),
        }
        if unit:
            sensor_data["unit"] = unit
        result[typ].append(sensor_data)
    return result


@spaceapi.get("/space.json")
async def space_json():
    data = {
        "api": "0.13",
        "api_compatibility": ["14"],
        "space": "Leigh Hackspace",
        "logo": "https://raw.githubusercontent.com/leigh-hackspace/logos-graphics-assets/master/logo/rose_logo.svg",
        "url": "http://leighhack.org",
        "location": {
            "address": "Unit 3.14, 3rd Floor, Leigh Spinners Mill, Park Lane, Leigh, WN7 2LB, United Kingdom",
            "lat": 53.493012,
            "lon": -2.493010,
            "timezone": "Europe/London",
        },
        "contact": {
            "email": "info@leighhack.org",
            "twitter": "@leigh_hackspace",
            "mastodon": "@leigh_hackspace@mastodon.social",
            "facebook": "https://www.facebook.com/groups/leighhackspace/",
        },
        "issue_report_channels": ["email"],
        "feeds": {
            "calendar": {
                "type": "ical",
                "url": urljoin(settings.base_url, '/events.ics'),
            }
        },
        "state": get_state(),
        "sensors": get_sensors(),
    }

    return data
