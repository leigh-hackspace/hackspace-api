from pydantic import BaseSettings


class Settings(BaseSettings):
    base_url: str = "http://localhost:8000"
    prometheus_instance: str = "http://localhost:9090"
    homeassistant_instance: str = "http://localhost:8123"
    homeassistant_token: str

    hackspace_address: str = "Unit 3.14, 3rd Floor, Leigh Spinners Mill, Park Lane, Leigh, WN7 2LB, United Kingdom"
    hackspace_address_lat: float = 53.493012
    hackspace_address_lon: float = -2.493010
    hackspace_timezone: str = "Europe/London"

    hackspace_open_entity: str = "binary_sensor.hackspace_open_multi"
    hackspace_public_calendar: str = "calendar.public_events"
    hackspace_member_calendar: str = "calendar.member_events"

    sensors_pressure_enabled: bool = False

settings = Settings()
