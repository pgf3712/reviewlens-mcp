from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REVIEWLENS_", env_file=".env", extra="ignore")

    mode: Literal["mock", "live"] = "mock"
    github_token: str | None = Field(default=None, repr=False)
    http_timeout_seconds: float = Field(default=10.0, ge=1, le=30)
    max_diff_chars: int = Field(default=120_000, ge=1_000, le=500_000)
    log_level: str = "INFO"
