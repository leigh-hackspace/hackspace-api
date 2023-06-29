from pydantic import BaseSettings


class Settings(BaseSettings):
    prometheus_instance: str = "http://10.3.1.30:9090"


settings = Settings()
