from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    database_host: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str

    # class Config:
    #     env_file = "../.env"

    model_config = SettingsConfigDict(
        env_file="../.env",
        extra="ignore"
    )


settings = Settings()
