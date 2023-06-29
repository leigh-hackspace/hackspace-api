# -*- coding: utf-8 -*-
from fastapi import APIRouter
from .prometheus import get_prometheus_metric
from cachetools.func import ttl_cache

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

@ttl_cache(ttl=60)
def get_open_status():
    res = get_prometheus_metric(
        'sum(homeassistant_input_boolean_state{entity="input_boolean.hackspace_open"})'
    )
    if res:
        return int(res["result"][0]["value"][1]) > 0
    return False

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
        "state": {
            "open": get_open_status(),
        },
        "sensors": get_sensors(),
    }

    return data
