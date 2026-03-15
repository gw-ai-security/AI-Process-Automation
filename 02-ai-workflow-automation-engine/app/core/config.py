"""Application configuration."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    app_name: str = Field(default="AI Workflow Automation Engine", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    postgres_db: str = Field(default="workflow_automation", alias="POSTGRES_DB")
    postgres_user: str = Field(default="workflow_user", alias="POSTGRES_USER")
    postgres_password: str = Field(default="workflow_password", alias="POSTGRES_PASSWORD")
    postgres_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, alias="POSTGRES_PORT")
    database_url: str = Field(
        default="postgresql://workflow_user:workflow_password@localhost:5432/workflow_automation",
        alias="DATABASE_URL",
    )
    llm_mode: str = Field(default="mock", alias="LLM_MODE")
    llm_base_url: str = Field(default="https://api.openai.com/v1", alias="LLM_BASE_URL")
    llm_api_key: str = Field(default="", alias="LLM_API_KEY")
    llm_model: str = Field(default="gpt-4o-mini", alias="LLM_MODEL")
    manual_baseline_minutes: int = Field(default=20, alias="MANUAL_BASELINE_MINUTES")
    automated_minutes: int = Field(default=5, alias="AUTOMATED_MINUTES")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Cache settings for application reuse."""
    return Settings()
