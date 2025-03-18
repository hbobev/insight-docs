from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    PROJECT_NAME: str = "InsightDocs"

    class Config:
        case_sensitive = True


# Create settings instance
settings = Settings()
