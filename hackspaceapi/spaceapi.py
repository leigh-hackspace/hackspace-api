from urllib.parse import urljoin

import arrow
from cachetools.func import ttl_cache
from fastapi import APIRouter

from .config import settings
from .services.homeassistant import get_entity_state

spaceapi = APIRouter()

# Sensors to export to the Space API
# entity_id, override_name
SENSORS = (
    ('sensor.gw_dhcp_leases_online', 'WiFi Clients'),
    ('sensor.bluetooth_proxy_temperature', 'Rack 1'),
    ('sensor.bluetooth_proxy_humidity', 'Rack 1'),
    ('weather.forecast_leigh_hackspace', 'Outside')
)

def get_state() -> dict:
    data = get_entity_state(settings.hackspace_open_entity)

    return {
        'open': data['state'] == 'on',
        'lastchange': int(arrow.get(data['last_changed']).timestamp()),
    }

@ttl_cache(ttl=60)
def get_sensors() -> dict:
    results = {}
    for sensor, override_name in SENSORS:
        data = get_entity_state(sensor)

        # Temperature sensor
        if ('device_class' in data['attributes'] and data['attributes']['device_class'] == 'temperature') or 'temperature' in data['attributes']:
            if 'temperature' not in results:
                results['temperature'] = []

            # Handle entities with temp attributes
            if 'temperature' in data['attributes']:
                value = float(data['attributes']['temperature'])
                unit_val = data['attributes']['temperature_unit']
            else:
                value = float(data['state'])
                unit_val = data['attributes']['unit_of_measurement']

            results['temperature'].append({
                'value': value,
                'unit': unit_val,
                'location': override_name or data['attributes']['friendly_name'],
                'lastchange': int(arrow.get(data['last_changed']).timestamp()),
            })

        # Humidity sensor
        if ('device_class' in data['attributes'] and data['attributes']['device_class'] == 'humidity') or 'humidity' in data['attributes']:
            if 'humidity' not in results:
                results['humidity'] = []

            # Handle entities with humidity attributes
            if 'humidity' in data['attributes']:
                value = float(data['attributes']['humidity'])
                unit_val = '%'  # Humidity attributes generally don't have a unit value, assume %
            else:
                value = float(data['state'])
                unit_val = data['attributes']['unit_of_measurement']

            results['humidity'].append({
                'value': value,
                'unit': unit_val,
                'location': override_name or data['attributes']['friendly_name'],
                'lastchange': int(arrow.get(data['last_changed']).timestamp()),
            })

        # Pressure sensor
        if ('device_class' in data['attributes'] and data['attributes']['device_class'] == 'pressure') or 'pressure' in data['attributes']:
            if 'barometer' not in results:
                results['barometer'] = []

            # Handle entities with temp attributes
            if 'pressure' in data['attributes']:
                value = float(data['attributes']['pressure'])
                unit_val = data['attributes']['pressure_unit']
            else:
                value = float(data['state'])
                unit_val = data['attributes']['unit_of_measurement']

            if settings.sensors_pressure_enabled:
                results['barometer'].append({
                    'value': value,
                    'unit': unit_val,
                    'location': override_name or data['attributes']['friendly_name'],
                    'lastchange': int(arrow.get(data['last_changed']).timestamp()),
                })

        # Network connections
        if 'unit_of_measurement' in data['attributes'] and data['attributes']['unit_of_measurement'] == 'clients':

            if 'network_connections' not in results:
                results['network_connections'] = []

            if data['state'] == 'unavailable':
                state = 0
            else:
                state = int(data['state'])
            
            results['network_connections'].append({
                'value': state,
                'location': override_name or data['attributes']['friendly_name'],
                'lastchange': int(arrow.get(data['last_changed']).timestamp()),
            })

    return results

@spaceapi.get("/space.json", description='Returns a SpaceAPI JSON supporting v13 and v14 of the schema', tags=['SpaceAPI'])
async def space_json():
    data = {
        "api": "0.13",
        "api_compatibility": ["14"],
        "space": "Leigh Hackspace",
        "logo": "https://raw.githubusercontent.com/leigh-hackspace/logos-graphics-assets/master/logo/rose_logo.svg",
        "url": "http://leighhack.org",
        "location": {
            "address": settings.hackspace_address,
            "lat": settings.hackspace_address_lat,
            "lon": settings.hackspace_address_lon,
            "timezone": settings.hackspace_timezone,
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
