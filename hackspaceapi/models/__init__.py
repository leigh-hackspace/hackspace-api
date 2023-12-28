from pydantic import BaseModel, Field

from hackspaceapi import VERSION


class HealthResponseModel(BaseModel):
    health: str = Field(description="State of the API", examples=["ok", "error"])
    version: str = Field(description="Version of the API", examples=[VERSION])
