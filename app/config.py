import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "FastAPI DevOps Demo")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://app_user:app_password@localhost:5432/app_db",
    )


def get_settings() -> Settings:
    return Settings()
