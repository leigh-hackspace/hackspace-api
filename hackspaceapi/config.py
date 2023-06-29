from pydantic import BaseSettings


class Settings(BaseSettings):
    prometheus_instance: str = "http://localhost:9090"


settings = Settings()
