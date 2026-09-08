from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    database_host: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    client_id: str
    client_secret: str
    session_secret_key: str
    class Config:
        env_file = "../.env"


settings = Settings()
