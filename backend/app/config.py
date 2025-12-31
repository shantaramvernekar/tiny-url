from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "tiny_url"
    redis_url: str = "redis://localhost:6379/0"
    base_url: str = "http://localhost:8000"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
