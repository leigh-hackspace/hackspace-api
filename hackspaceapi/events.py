from datetime import datetime
from enum import Enum
from typing import List, Literal

import arrow
from fastapi import APIRouter, Response
from ics import Calendar, Event

from hackspaceapi import VERSION

from .config import settings
from .services.homeassistant import call_homeassistant

events = APIRouter()


class CalendarType(str, Enum):
    public = settings.hackspace_public_calendar
    members = settings.hackspace_member_calendar


def get_calendar_events(start: datetime, end: datetime, calendar: str) -> List:
    print(call_homeassistant("/api/calendars"))
    data = call_homeassistant("/api/calendars/{0}".format(calendar.value), start=start, end=end)
    if data:
        for event in data:
            event["calendar"] = calendar
        return data
    return []


@events.get(
    "/events",
    description="Returns a list of upcoming events in a JSON format",
    tags=["Events"],
)
async def get_events(
    start: datetime | None = arrow.utcnow().datetime,
    end: datetime | None = arrow.utcnow().shift(days=30).datetime,
    calendar: Literal["public", "members"] = "public",
):
    return get_calendar_events(start, end, CalendarType[calendar])


@events.get(
    "/events.ics",
    description="Returns a list of upcoming events in a iCal format",
    tags=["Events"],
)
async def get_events_ics(
    start: datetime | None = arrow.utcnow().datetime,
    end: datetime | None = arrow.utcnow().shift(days=30).datetime,
    calendar: Literal["public", "members"] = "public",
):
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
        )
        cal.events.add(evt)

    return Response(content=cal.serialize(), media_type="text/calendar")
