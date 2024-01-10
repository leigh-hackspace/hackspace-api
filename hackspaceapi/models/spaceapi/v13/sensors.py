from typing import Optional, List
from enum import Enum
from pydantic import BaseModel
from pydantic_extra_types.mac_address import MacAddress


class SpaceAPIv13BaseSensorModel(BaseModel):
    value: float
    location: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


class TemperatureUnitEnum(str, Enum):
    celsius = "°C"
    fahrenheit = "°F"
    kelvin = "K"
    delisle = "°De"
    newton = "°N"
    rankine = "°R"
    reaumur = "°Ré"
    romer = "°Rø"


class SpaceAPIv13TemperatureSensorModel(SpaceAPIv13BaseSensorModel):
    unit: TemperatureUnitEnum
    location: str


class PressureUnitEnum(str, Enum):
    hectopascal = "hPa"


class SpaceAPIv13BarometerSensorModel(SpaceAPIv13BaseSensorModel):
    unit: PressureUnitEnum
    location: str


class RadiationUnitEnum(str, Enum):
    cpm = "cpm"
    rh = "r/h"
    usvh = "µSv/h"
    msva = "mSv/a"
    usva = "µSv/a"


class SpaceAPIv13RadiationTypeSensorModel(SpaceAPIv13BaseSensorModel):
    unit: RadiationUnitEnum
    dead_time: Optional[float] = None
    conversion_factor: Optional[float] = None


class SpaceAPIv13RadiationSensorModel(SpaceAPIv13BaseSensorModel):
    alpha: Optional[List[SpaceAPIv13RadiationTypeSensorModel]] = None
    beta: Optional[List[SpaceAPIv13RadiationTypeSensorModel]] = None
    gamma: Optional[List[SpaceAPIv13RadiationTypeSensorModel]] = None
    beta_gamma: Optional[List[SpaceAPIv13RadiationTypeSensorModel]] = None


class HumidityUnitEnum(str, Enum):
    relative_humidity = "%"


class SpaceAPIv13HumiditySensorModel(SpaceAPIv13BaseSensorModel):
    unit: HumidityUnitEnum
    location: str


class BeverageUnitEnum(str, Enum):
    bottle = "btl"
    crate = "crt"


class SpaceAPIv13BeverageSupplySensorModel(SpaceAPIv13BaseSensorModel):
    unit: BeverageUnitEnum


class PowerConsumptionUnitEnum(str, Enum):
    millawatt = "mW"
    watt = "W"
    voltage_amps = "VA"


class SpaceAPIv13PowerConsumptionSensorModel(SpaceAPIv13BaseSensorModel):
    unit: PowerConsumptionUnitEnum


class WindSpeedUnitEnum(str, Enum):
    meters_second = "m/s"
    kilometers_hour = "km/h"
    knots = "kn"


class SpaceAPIv13WindSpeedSensorPropertyModel(BaseModel):
    value: float
    unit: WindSpeedUnitEnum


class WindDirectionUnitEnum(str, Enum):
    degrees = "°"


class SpaceAPIv13WindDirectionPropertyModel(BaseModel):
    value: float
    unit: WindDirectionUnitEnum


class WindElevationUnitEnum(str, Enum):
    meters = "m"


class SpaceAPIv13WindElevationPropertyModel(BaseModel):
    value: float
    unit: WindElevationUnitEnum


class SpaceAPIv13WindSensorPropertiesModel(BaseModel):
    speed: SpaceAPIv13WindSpeedSensorPropertyModel
    gust: SpaceAPIv13WindSpeedSensorPropertyModel
    direction: SpaceAPIv13WindDirectionPropertyModel
    elevation: SpaceAPIv13WindElevationPropertyModel


class SpaceAPIv13WindSensorModel(SpaceAPIv13BaseSensorModel):
    properties: SpaceAPIv13WindSensorPropertiesModel


class NetworkConnectionTypeEnum(str, Enum):
    wifi = "wifi"
    cable = "cable"
    spacenet = "spacenet"


class SpaceAPIv13MachineModel(BaseModel):
    name: Optional[str] = None
    mac: MacAddress


class SpaceAPIv13NetworkConnectionSensorModel(SpaceAPIv13BaseSensorModel):
    type: NetworkConnectionTypeEnum
    machines: Optional[List[SpaceAPIv13MachineModel]] = None


class SpaceAPIv13AccountBalanceSensorModel(SpaceAPIv13BaseSensorModel):
    unit: str


class SpaceAPIv13TotalMemberCountSensorModel(SpaceAPIv13BaseSensorModel):
    pass


class SpaceAPIv13PeoplePresentSensorModel(SpaceAPIv13BaseSensorModel):
    names: Optional[List[str]] = None
