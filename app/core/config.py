from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    env: str
    debug: bool

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # 👈 CLAVE
    )


settings = Settings()
