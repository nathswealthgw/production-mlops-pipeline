from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_env: str = Field(default="development")
    app_name: str = Field(default="mlops-production-pipeline")
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])
    model_artifact_path: str = Field(default="ml/training/artifacts/model.joblib")
    model_version: str = Field(default="v1.0.0")
    hmac_secret: str = Field(default="change-me")


settings = Settings()
