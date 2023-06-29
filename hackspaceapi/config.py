from pydantic import BaseSettings


class Settings(BaseSettings):
    base_url: str = "http://localhost:8000"
    prometheus_instance: str = "http://localhost:9090"
    homeassistant_instance: str = "http://localhost:8123"
    homeassistant_token: str
    hackspace_open_entity: str = 'input_boolean.hackspace_open'

settings = Settings()
