from datetime import datetime
from enum import Enum
from typing import Iterable, Literal

import arrow
from fastapi import APIRouter, Response
from ics import Calendar, Event

from hackspaceapi import VERSION

from .models.config import settings
from .services.homeassistant import call_homeassistant

events = APIRouter()


class CalendarType(str, Enum):
    public = settings.hackspace_public_calendar
    members = settings.hackspace_member_calendar


def get_calendar_events(start: datetime, end: datetime, calendar: str) -> Iterable:
    """
    Get a list of calendar events from Home Assistant via the API.
    """
    data = call_homeassistant(
        "/api/calendars/{0}".format(calendar.value), start=start, end=end
    )
    if data:
        for event in data:
            event["calendar"] = calendar
        return data
    return []


@events.get(
    "/events",
    summary="Get upcoming events",
    description="Returns a list of upcoming events in a JSON format",
    tags=["Events"],
)
async def get_events(
    start: datetime | None = None,
    end: datetime | None = None,
    calendar: Literal["public", "members"] = "public",
):
    if not start:
        start = arrow.utcnow().datetime
    if not end:
        end = arrow.utcnow().shift(days=30).datetime

    return get_calendar_events(start, end, CalendarType[calendar])


@events.get(
    "/events.ics",
    summary="Get upcoming events in iCal format",
    description="Returns a list of upcoming events in a iCal format",
    tags=["Events"],
)
async def get_events_ics(
    start: datetime | None = None,
    end: datetime | None = None,
    calendar: Literal["public", "members"] = "public",
):
    if not start:
        start = arrow.utcnow().datetime
    if not end:
        end = arrow.utcnow().shift(days=30).datetime

    data = get_calendar_events(start, end, CalendarType[calendar])

    cal = Calendar(creator="Hackspace API {0}".format(VERSION))
    for event in data:
        # If its a recurring event, tag on the ID to the end of the UID
        if "recurrence_id" in event and event["recurrence_id"]:
            uid = event["uid"] + "-" + event["recurrence_id"]
        else:
            uid = event["uid"]

        evt = Event(
            event["summary"],
            begin=event["start"]["dateTime"],
            end=event["end"]["dateTime"],
            description=event["description"],
            uid=uid,
            location=settings.hackspace_address,
            geo=(settings.hackspace_address_lat, settings.hackspace_address_lon),
        )
        cal.events.add(evt)

    return Response(content=cal.serialize(), media_type="text/calendar")
