from typing import List, Optional

import yaml
from pydantic import BaseModel, Field


class HomeassistantSensorModel(BaseModel):
    entity: str
    name: Optional[str] = None
    location: str
    unit: Optional[str] = None


class PrometheusSensorModel(BaseModel):
    query: str
    name: str
    location: Optional[str] = None
    sensor_type: str
    unit: Optional[str] = None


class SensorSettingsModel(BaseModel):
    homeassistant: List[HomeassistantSensorModel] = Field(
        description="A list of sensors from Home Assistant"
    )
    prometheus: List[PrometheusSensorModel] = Field(
        description="A list of sensors from Prometheus"
    )

    @staticmethod
    def load_from_yaml(filename: str) -> BaseModel:
        with open(filename, "r") as fobj:
            data = yaml.safe_load(fobj)
        return SensorSettingsModel(**data)
