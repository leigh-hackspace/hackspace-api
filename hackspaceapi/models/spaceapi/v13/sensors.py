from typing import Optional, List
from pydantic import BaseModel


class SpaceAPIv13BaseSensorModel(BaseModel):
    value: float
    location: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


class SpaceAPIv13TemperatureSensorModel(SpaceAPIv13BaseSensorModel):
    unit: str
    location: str


class SpaceAPIv13BarometerSensorModel(SpaceAPIv13BaseSensorModel):
    unit: str
    location: str


class SpaceAPIv13RadiationTypeSensorModel(SpaceAPIv13BaseSensorModel):
    unit: str
    dead_time: Optional[float] = None
    conversion_factor: Optional[float] = None


class SpaceAPIv13RadiationSensorModel(SpaceAPIv13BaseSensorModel):
    alpha: Optional[List[SpaceAPIv13RadiationTypeSensorModel]] = None
    beta: Optional[List[SpaceAPIv13RadiationTypeSensorModel]] = None
    gamma: Optional[List[SpaceAPIv13RadiationTypeSensorModel]] = None
    beta_gamma: Optional[List[SpaceAPIv13RadiationTypeSensorModel]] = None


class SpaceAPIv13HumiditySensorModel(SpaceAPIv13BaseSensorModel):
    unit: str = "%"
    location: str


class SpaceAPIv13BeverageSupplySensorModel(SpaceAPIv13BaseSensorModel):
    unit: str = "btl"


class SpaceAPIv13PowerConsumptionSensorModel(SpaceAPIv13BaseSensorModel):
    unit: str


class SpaceAPIv13WindSensorPropertyModel(BaseModel):
    value: float
    unit: str


class SpaceAPIv13WindSensorPropertiesModel(BaseModel):
    speed: SpaceAPIv13WindSensorPropertyModel
    gust: SpaceAPIv13WindSensorPropertyModel
    direction: SpaceAPIv13WindSensorPropertyModel
    elevation: SpaceAPIv13WindSensorPropertyModel


class SpaceAPIv13WindSensorModel(SpaceAPIv13BaseSensorModel):
    properties: SpaceAPIv13WindSensorPropertiesModel


class SpaceAPIv13NetworkConnectionSensorModel(SpaceAPIv13BaseSensorModel):
    type: str
    machines: Optional[dict] = None


class SpaceAPIv13AccountBalanceSensorModel(SpaceAPIv13BaseSensorModel):
    unit: str


class SpaceAPIv13TotalMemberCountSensorModel(SpaceAPIv13BaseSensorModel):
    pass


class SpaceAPIv13PeoplePresentSensorModel(SpaceAPIv13BaseSensorModel):
    names: Optional[List[str]] = None
