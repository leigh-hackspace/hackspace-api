import logging
from urllib.parse import urljoin

import arrow
from cachetools.func import ttl_cache
from fastapi import APIRouter

from .models.config import settings
from .models.sensors import SensorSettingsModel
from .models.spaceapi.v14_lhs import SpaceAPIv14LHSModel
from .services.homeassistant import get_entity_state
from .services.prometheus import get_prometheus_metric
from .services.website import get_membership_data

spaceapi = APIRouter()


def get_state() -> dict:
    """
    Return the current open state of the Hackspace.
    """
    data = get_entity_state(settings.hackspace_open_entity)
    if data:
        return {
            "open": data["state"] == "on",
            "lastchange": int(arrow.get(data["last_changed"]).timestamp()),
        }

    # We didn't get a valid response from Home Assistant, assume we're closed
    return {
        "open": False,
    }


@ttl_cache(ttl=60)
def get_sensors() -> dict:
    """
    Query Home Assistant and Prometheus to build the 'sensors' section of the
    SpaceAPI response.
    """
    results = {}

    # Load the sensor config if its not initialized
    if not settings.sensor_config:
        settings.sensor_config = SensorSettingsModel.load_from_yaml(
            settings.sensor_config_file
        )

    for sensor in settings.sensor_config.homeassistant:
        data = get_entity_state(sensor.entity)
        if not data:
            logging.warning(
                "Call for {0} sensor returned an empty result, skipping".format(
                    sensor.entity
                )
            )
            continue

        # Temperature sensor
        if (
            "device_class" in data["attributes"]
            and data["attributes"]["device_class"] == "temperature"
        ) or "temperature" in data["attributes"]:
            if "temperature" not in results:
                results["temperature"] = []

            # Handle entities with temp attributes
            if "temperature" in data["attributes"]:
                try:
                    value = float(data["attributes"]["temperature"])
                except ValueError:
                    logging.warning(
                        "Failed to convert '{0}' to float, so skipping sensor {1}".format(
                            data["attributes"]["temperature"],
                            sensor.location or data["attributes"]["friendly_name"],
                        )
                    )
                    continue
                unit_val = data["attributes"]["temperature_unit"]
            else:
                try:
                    value = float(data["state"])
                except ValueError:
                    logging.warning(
                        "Failed to convert '{0}' to float, so skipping sensor {1}".format(
                            data["state"],
                            sensor.location or data["attributes"]["friendly_name"],
                        )
                    )
                    continue
                unit_val = data["attributes"]["unit_of_measurement"]

            results["temperature"].append(
                {
                    "value": value,
                    "unit": sensor.unit or unit_val,
                    "location": sensor.location or data["attributes"]["friendly_name"],
                    "lastchange": int(arrow.get(data["last_changed"]).timestamp()),
                }
            )

        # Humidity sensor
        if (
            "device_class" in data["attributes"]
            and data["attributes"]["device_class"] == "humidity"
        ) or "humidity" in data["attributes"]:
            if "humidity" not in results:
                results["humidity"] = []

            # Handle entities with humidity attributes
            if "humidity" in data["attributes"]:
                value = float(data["attributes"]["humidity"])
                unit_val = "%"  # Humidity attributes generally don't have a unit value, assume %
            else:
                try:
                    value = float(data["state"])
                except ValueError:
                    logging.warning(
                        "Failed to convert '{0}' to float, so skipping sensor {1}".format(
                            data["state"],
                            sensor.location or data["attributes"]["friendly_name"],
                        )
                    )
                    continue
                unit_val = data["attributes"]["unit_of_measurement"]

            results["humidity"].append(
                {
                    "value": value,
                    "unit": sensor.unit or unit_val,
                    "location": sensor.location or data["attributes"]["friendly_name"],
                    "lastchange": int(arrow.get(data["last_changed"]).timestamp()),
                }
            )

        # Pressure sensor
        if (
            "device_class" in data["attributes"]
            and data["attributes"]["device_class"] == "pressure"
        ) or "pressure" in data["attributes"]:
            if "barometer" not in results:
                results["barometer"] = []

            # Handle entities with temp attributes
            if "pressure" in data["attributes"]:
                value = float(data["attributes"]["pressure"])
                unit_val = data["attributes"]["pressure_unit"]
            else:
                value = float(data["state"])
                unit_val = data["attributes"]["unit_of_measurement"]

            if settings.sensors_pressure_enabled:
                results["barometer"].append(
                    {
                        "value": value,
                        "unit": sensor.unit or unit_val,
                        "location": sensor.location
                        or data["attributes"]["friendly_name"],
                        "lastchange": int(arrow.get(data["last_changed"]).timestamp()),
                    }
                )

        # Network connections
        if (
            "unit_of_measurement" in data["attributes"]
            and data["attributes"]["unit_of_measurement"] == "clients"
        ):
            if "network_connections" not in results:
                results["network_connections"] = []

            if data["state"] == "unavailable":
                state = 0
            else:
                state = int(data["state"])

            results["network_connections"].append(
                {
                    "type": "wifi",
                    "value": state,
                    "location": sensor.location or data["attributes"]["friendly_name"],
                    "lastchange": int(arrow.get(data["last_changed"]).timestamp()),
                }
            )

        # 3D printers - FIXME: need a better way to detect this!
        if (
            "icon" in data["attributes"]
            and data["attributes"]["icon"] == "mdi:printer-3d"
        ):
            if "ext_3d_printers" not in results:
                results["ext_3d_printers"] = []

            if data["state"] == "unavailable":
                state = "offline"
            else:
                state = data["state"].lower()

            results["ext_3d_printers"].append(
                {
                    "name": sensor.name
                    or sensor.location
                    or data["attributes"]["friendly_name"].split()[0],
                    "state": state,
                    "lastchange": int(arrow.get(data["last_changed"]).timestamp()),
                }
            )

    for sensor in settings.sensor_config.prometheus:
        data = get_prometheus_metric(sensor.query)
        if not data or "result" not in data or len(data["result"]) == 0:
            logging.warning(
                "Call for {0} sensor returned an empty result, skipping".format(
                    sensor.name
                )
            )
            continue

        if sensor.sensor_type not in results:
            results[sensor.sensor_type] = []

        if sensor.sensor_type == "total_member_count":
            results["total_member_count"].append(
                {
                    "value": int(data["result"][0]["value"][1]),
                    "name": sensor.name,
                    "lastchange": int(data["result"][0]["value"][0]),
                }
            )

    return results


def get_links() -> list:
    """
    Return a list of links to add to the 'links' value of the SpaceAPI response.
    """
    return [
        {"name": "Github", "url": "https://github.com/leigh-hackspace"},
        {
            "name": "Slack",
            "url": "https://join.slack.com/t/leighhack/shared_invite/enQtNDYzMjEyMDMxNDExLTE1MWY5N2IwMzdhMzQ0ZWFiNDkyNzJmMGM1ZmFkODcwMGM5ODFmYmI4MjhmM2JiMWEyY2E3NTRjMTQzMzljZWU",
        },
        {"name": "Discourse", "url": "https://discourse.leighhack.org/"},
        {"name": "Join Leigh Hackspace", "url": "https://leighhack.org/membership/"},
    ]


def get_membership_plans() -> list:
    """
    Format the website membership plan data into a SpaceAPI compatible format.
    """
    data = get_membership_data()
    if not data:
        return []

    output = []
    for plan in data:
        if int(plan["value"]) == 0:
            continue
        newplan = {}
        for key in plan.keys():
            if key not in [
                "name",
                "value",
                "currency",
                "billing_interval",
                "description",
            ]:
                newplan["ext_{0}".format(key)] = plan[key]
            else:
                newplan[key] = plan[key]

        output.append(newplan)
    return output


@spaceapi.get(
    "/space.json",
    summary="Get Space API JSON",
    description="Returns a SpaceAPI JSON supporting v13 and v14 of the schema",
    tags=["SpaceAPI"],
    response_model=SpaceAPIv14LHSModel,
    response_model_exclude_none=True,
)
async def space_json() -> SpaceAPIv14LHSModel:
    data = {
        "api": "0.13",
        "api_compatibility": ["13", "14"],
        "space": settings.hackspace_name,
        "logo": settings.hackspace_logo_url,
        "url": settings.hackspace_website_url,
        "location": {
            "address": settings.hackspace_address,
            "lat": settings.hackspace_address_lat,
            "lon": settings.hackspace_address_lon,
            "timezone": settings.hackspace_timezone,
            "ext_osm_node": settings.hackspace_osm_node,
        },
        "state": get_state(),
        "contact": {
            "email": "info@leighhack.org",
            "twitter": "@leigh_hackspace",
            "mastodon": "@leigh_hackspace@mastodon.social",
            "facebook": "https://www.facebook.com/groups/leighhackspace/",
            "ext_instagram": "leighhackspace",
            "ext_slack": "leighhack.slack.com",
        },
        "sensors": get_sensors(),
        "feeds": {
            "blog": {
                "type": "rss",
                "url": "https://leighhack.org/blog/index.xml",
            },
            "calendar": {
                "type": "ical",
                "url": urljoin(str(settings.base_url), "/events.ics"),
            },
        },
        "links": get_links(),
        "issue_report_channels": ["email"],
        "membership_plans": get_membership_plans(),
        "ext_dabo": "Dabo!",
    }

    return data
