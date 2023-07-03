from urllib.parse import urljoin

import arrow
from cachetools.func import ttl_cache
from fastapi import APIRouter

from .config import settings
from .services.homeassistant import get_entity_state
from .services.prometheus import get_prometheus_metric

spaceapi = APIRouter()

# Homeassistant Sensors to export to the Space API
# entity_id, override_name
HOMEASSISTANT_SENSORS = (
    ('sensor.gw_dhcp_leases_online', 'WiFi Clients'),
    ('sensor.bluetooth_proxy_temperature', 'Rack 1'),
    ('sensor.bluetooth_proxy_humidity', 'Rack 1'),
    ('weather.forecast_leigh_hackspace', 'Outside')
)

# Prometheus queries to export to the Space API
# query, override_name, type
PROMETHEUS_SENSORS = (
    ('gocardless_members_count{}', 'Active Members', 'total_member_count'),
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
    for sensor, override_name in HOMEASSISTANT_SENSORS:
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

    for query, override_name, sensor_type in PROMETHEUS_SENSORS:
        data = get_prometheus_metric(query)

        if sensor_type not in results:
            results[sensor_type] = []

        if sensor_type == 'total_member_count':
            results['total_member_count'].append({
                'value': data['result'][0]['value'][1],
                'name': override_name,
                'lastchange': int(data['result'][0]['value'][0]),
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
