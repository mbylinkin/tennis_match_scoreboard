from pydantic import MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.constants import Environment
import pymysql

pymysql.install_as_MySQLdb()


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DATABASE_URL: MySQLDsn
    SITE_DOMAIN: str = "myapp.com"
    ENVIRONMENT: Environment = Environment.PRODUCTION
    APP_VERSION: str = "1"


settings = Config()
