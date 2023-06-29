from datetime import datetime, timedelta

from fastapi import APIRouter, Response
from ics import Calendar, Event

from .homeassistant import call_homeassistant

events = APIRouter()


def get_calendar_events(start=datetime.utcnow(), end=datetime.utcnow() + timedelta(30)):
    calendars = call_homeassistant("/api/calendars")
    entities = [cal["entity_id"] for cal in calendars]

    events = []
    for calendar in entities:
        data = call_homeassistant(
            "/api/calendars/{0}".format(calendar), start=start, end=end
        )
        events.extend(data)

    return events


@events.get("/events")
async def get_events():
    return get_calendar_events()


@events.get("/events.ics")
async def get_events_ics():
    data = get_calendar_events()

    cal = Calendar()
    for event in data:
        evt = Event(
            event["summary"],
            begin=event["start"]["dateTime"],
            end=event["end"]["dateTime"],
            description=event["description"],
            uid=event["uid"],
        )
        cal.events.add(evt)

    return Response(content=cal.serialize())
