from enum import Enum

from pydantic import BaseModel, Field

from hackspaceapi import VERSION


class HealthStateEnum(str, Enum):
    ok = "ok"
    error = "error"


class HealthResponseModel(BaseModel):
    health: HealthStateEnum = Field(
        description="State of the API", examples=["ok", "error"]
    )
    version: str = Field(description="Version of the API", examples=[VERSION])
