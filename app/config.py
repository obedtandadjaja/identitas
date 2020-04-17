import os

from pydantic import BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
   
    SECRET_KEY: str

    SENTRY_DSN: HttpUrl = None

    # Postgres
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_URI: PostgresDsn = None

    @validator("POSTGRES_URI", pre=True)
    def db_connection(cls, v, values):
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # App-specific
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

settings = Settings()
