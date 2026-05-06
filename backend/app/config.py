from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "OfferCopilot API"
    database_url: str = "sqlite:///./offercopilot.db"
    frontend_origin: str = "http://localhost:3000"
    search_max_results: int = 10
    fetch_timeout_seconds: int = 15
    min_sources_for_confident_report: int = 3

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
