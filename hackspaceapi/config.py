from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    base_url: str = "http://localhost:8000"
    
    # External app config
    prometheus_instance: str = "http://prometheus:9090"
    homeassistant_instance: str = "http://homeassistant:8123"
    homeassistant_token: str
    authentik_instance: str = "http://localhost:9000"
    authentik_token: str
    authentik_uid_attribute: str = 'leighhack.org/door_access_uid'
    authentik_user_path: str = 'users'

    hackspace_name: str = "Leigh Hackspace"
    hackspace_logo_url: str = "https://raw.githubusercontent.com/leigh-hackspace/logos-graphics-assets/master/logo/rose_logo.svg"
    hackspace_website_url: str = "https://leighhack.org"
    hackspace_address: str = "Leigh Hackspace, Unit 3.14, 3rd Floor, Leigh Spinners Mill, Park Lane, Leigh, WN7 2LB, United Kingdom"
    hackspace_address_lat: float = 53.493012
    hackspace_address_lon: float = -2.493010
    hackspace_timezone: str = "Europe/London"

    hackspace_open_entity: str = "binary_sensor.hackspace_open_multi"
    hackspace_public_calendar: str = "calendar.public_events"
    hackspace_member_calendar: str = "calendar.member_events"

    hackspace_doors_allowed_group: str = 'Members'

    sensors_pressure_enabled: bool = False


settings = Settings()
