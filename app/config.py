from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Use model_config instead of class Config
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # pyright: ignore
