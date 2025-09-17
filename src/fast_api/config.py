from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import pathlib

class Settings(BaseSettings):
    # lowercase Python attribute, explicitly linked to uppercase env variable
    database_url: str = Field(..., env="DATABASE_URL")
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    REDIS_HOST:str = "localhost"
    REDIS_PORT: int =6379
    MAIL_USERNAME : str 
    MAIL_PASSWORD : str
    MAIL_FROM  : str
    MAIL_PORT: int
    MAIL_SERVER: str
    REDIS_URL: str = Field(default="redis://localhost:6379/0")


    model_config = SettingsConfigDict(
        env_file=f"{pathlib.Path(__file__).resolve().parent}/.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

config = Settings()

broker_url = config.REDIS_URL
result_backend = config.REDIS_URL
broker_connection_retry_on_startup = True