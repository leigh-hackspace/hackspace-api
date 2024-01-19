"""
SpaceAPI v14

https://github.com/SpaceApi/schema

Most models are inherited from v13, updated models have values overridden
"""

from typing import List, Optional

from enum import Enum
from pydantic import BaseModel, HttpUrl

from .v13 import (
    SpaceAPIv13LocationModel,
    SpaceAPIv13ContactModel,
    SpaceAPIv13KeymastersModel,
    SpaceAPIv13Model,
    SpaceAPIv13BaseSensorModel,
    SpaceAPIv13SensorsModel,
)


class SpaceAPIv14LocationModel(SpaceAPIv13LocationModel):
    timezone: Optional[str] = None


class SpaceAPIv14KeymastersModel(SpaceAPIv13KeymastersModel):
    xmpp: Optional[str] = None
    matrix: Optional[str] = None
    mastodon: Optional[str] = None
    mumble: Optional[str] = None


class SpaceAPIv14ContactModel(SpaceAPIv13ContactModel):
    keymasters: Optional[List[SpaceAPIv14KeymastersModel]] = None
    xmpp: Optional[str] = None
    matrix: Optional[str] = None
    mastodon: Optional[str] = None
    mumble: Optional[str] = None


class SpaceAPIv14LinkModel(BaseModel):
    name: str
    description: Optional[str] = None
    url: HttpUrl


class SpaceAPIv14NetworkTrafficSensorModel(SpaceAPIv13BaseSensorModel):
    properties: dict


class SpaceAPIv14SensorsModel(SpaceAPIv13SensorsModel):
    network_traffic: Optional[List[SpaceAPIv14NetworkTrafficSensorModel]] = None


class BillingIntervalEnum(str, Enum):
    yearly = "yearly"
    monthly = "monthly"
    weekly = "weekly"
    daily = "daily"
    hourly = "hourly"
    other = "other"


class SpaceAPIv14MembershipPlanModel(BaseModel):
    name: str
    value: int
    currency: str
    billing_interval: BillingIntervalEnum
    description: Optional[str] = None


class SpaceAPIv14SpacefedModel(BaseModel):
    spacenet: bool = False
    spacesaml: bool = False


class SpaceAPIv14Model(SpaceAPIv13Model):
    api_compatibility: List[str] = ["14"]
    location: SpaceAPIv14LocationModel
    spacefed: Optional[SpaceAPIv14SpacefedModel] = None
    contact: SpaceAPIv14ContactModel
    sensors: SpaceAPIv14SensorsModel
    links: Optional[List[SpaceAPIv14LinkModel]] = None
    membership_plans: Optional[List[SpaceAPIv14MembershipPlanModel]] = None
