"""
Leigh Hackspace modified version of the v14 SpaceAPI

* ext_osm_node to represent the Hackspace's node on OpenStreetMap
* ext_3d_printers sensors
* Additional fields to membership_plans
"""
from typing import Optional, List
from pydantic import BaseModel
from .v14 import (
    SpaceAPIv14Model,
    SpaceAPIv14ContactModel,
    SpaceAPIv14LocationModel,
    SpaceAPIv14SensorsModel,
    SpaceAPIv14MembershipPlanModel,
)


class SpaceAPIv14LHSContactModel(SpaceAPIv14ContactModel):
    ext_slack: Optional[str] = None
    ext_instagram: Optional[str] = None


class SpaceAPIv14LHS3DPrinterSensorModel(BaseModel):
    name: str
    state: str
    lastchange: int


class SpaceAPIv14LHSSensorsModel(SpaceAPIv14SensorsModel):
    ext_3d_printers: Optional[List[SpaceAPIv14LHS3DPrinterSensorModel]] = None


class SpaceAPIv14LHSLocationModel(SpaceAPIv14LocationModel):
    ext_osm_node: int


class SpaceAPIv14LHSMembershipPlanModel(SpaceAPIv14MembershipPlanModel):
    ext_link: Optional[str] = None


class SpaceAPIv14LHSModel(SpaceAPIv14Model):
    location: SpaceAPIv14LHSLocationModel
    contact: SpaceAPIv14LHSContactModel
    sensors: Optional[SpaceAPIv14LHSSensorsModel] = None
    membership_plans: Optional[List[SpaceAPIv14LHSMembershipPlanModel]] = None
    ext_dabo: str = "Dabo!"
