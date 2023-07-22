from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    base_url: str = Field(
        default="http://localhost:8000",
        description="URL base where the application will be accessible at",
    )

    prometheus_instance: str = Field(
        default="http://prometheus:9090",
        description="Endpoint URL for the Prometheus instance",
    )

    homeassistant_instance: str = Field(
        default="http://homeassistant:8123",
        description="Endpoint URL for the Home Assistant instance",
    )

    homeassistant_token: str = Field(
        description="Token used to access the Home Assistant API"
    )

    hackspace_name: str = Field(
        default="Leigh Hackspace", description="Name of the hackspace"
    )

    hackspace_logo_url: str = Field(
        default="https://raw.githubusercontent.com/leigh-hackspace/logos-graphics-assets/master/logo/rose_logo.svg",
        description="URL to the logo for the hackspace",
    )

    hackspace_website_url: str = Field(
        default="https://leighhack.org", description="URL to the hackspace's website"
    )

    hackspace_address: str = Field(
        default="Leigh Hackspace, Unit 3.14, 3rd Floor, Leigh Spinners Mill, Park Lane, Leigh, WN7 2LB, United Kingdom",
        description="Full address to the hackspace",
    )

    hackspace_address_lat: float = Field(
        default=53.493012, description="Latitude of the hackspace"
    )

    hackspace_address_lon: float = Field(
        default=-2.493010, description="Longitude of the hackspace"
    )

    hackspace_timezone: str = Field(
        default="Europe/London", description="Timezone the hackspace is located in"
    )

    hackspace_open_entity: str = Field(
        default="binary_sensor.hackspace_open_multi",
        description="Entity ID of the Home Assistant device to indicate open status",
    )

    hackspace_public_calendar: str = Field(
        default="calendar.public_events",
        description="The entity ID of the Home Assistant public calendar",
    )

    hackspace_member_calendar: str = Field(
        default="calendar.member_events",
        description="The entity ID of the Home Assistant member calendar",
    )

    sensors_pressure_enabled: bool = Field(
        default=False, description="Enable pressure sensors"
    )


settings = Settings()
