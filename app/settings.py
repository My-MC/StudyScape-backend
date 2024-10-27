from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_user: str
    db_password: str

    db_address: str
    db_namespace: str
    db_database: str
    model_config = SettingsConfigDict(env_file=".env")
