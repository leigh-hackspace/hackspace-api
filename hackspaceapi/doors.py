import logging
from urllib.parse import urljoin
from typing import Optional, List

import requests
from fastapi import APIRouter, status, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .config import settings


class AuthRequest(BaseModel):
    # Name of the endpoint door device
    door_id: str

    # The fob's UID
    uid: str

    # Represents a list of groups that are required for this request
    groups: List[str] = [settings.hackspace_doors_allowed_group]

    # Represents the card's content
    content: Optional[str] = None


doors = APIRouter()

# Generate session for accessing Authentik
session = requests.session()
session.headers = {"Authorization": "Bearer {0}".format(settings.authentik_token)}


def build_authentik_url(endpoint: str) -> str:
    return urljoin(settings.authentik_instance, "/api/v3/" + endpoint)


def log_door_access(door_id: str, user: dict):
    logging.info("Door Access Approved - {0} - {1}".format(door_id, user["name"]))


def return_fail(error_msg: str) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"fail": True, "error": error_msg},
    )


@doors.post("/auth")
async def authenticate(auth: AuthRequest, background_tasks: BackgroundTasks):
    try:
        resp = session.get(
            build_authentik_url("core/users/"), params={'type': 'default', 'path': settings.authentik_user_path}
        )
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.ReadTimeout,
    ) as exc:
        logging.exception(exc)
        return return_fail("Failed to connect to Authentik")

    except requests.exceptions.RequestException as exc:
        logging.exception(exc)
        return return_fail("Unknown issue connecting to Authentik")

    if resp.status_code != 200:
        logging.warning(
            "Non-200 response calling the users API: {0}".format(resp.status_code)
        )
        return return_fail("Non-200 response from Authentik")

    # Iterate the users in the response
    for user in resp.json()["results"]:
        if settings.authentik_uid_attribute not in user["attributes"]:
            continue

        logging.debug("Attributes: {0}".format(user["attributes"]))
        # Does this user have the UID we're looking for?
        if auth.uid not in user["attributes"][settings.authentik_uid_attribute]:
            continue

        # We've got one! ...but is it active?
        if not user["is_active"]:
            return return_fail("User is disabled")

        # Is the user a member of a allowed group?
        for group in user["groups_obj"]:
            if group["name"] in auth.groups:
                # Success! log and return a 200
                background_tasks.add_task(log_door_access, auth.door_id, user)
                return {"fail": False, "name": user["name"]}

        # If we don't match a group
        return return_fail("User is not a member of {0}".format(auth.groups))

    # If we can't match a user to the UID
    return return_fail("No user found for UID")
