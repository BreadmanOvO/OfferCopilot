from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root: backend/app/config.py -> backend -> OfferCopilot
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_ENV_FILE = _PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    app_name: str = "OfferCopilot API"
    database_url: str = "sqlite:///./offercopilot.db"
    frontend_origin: str = "http://localhost:3000"
    search_max_results: int = 10
    fetch_timeout_seconds: int = 15
    min_sources_for_confident_report: int = 3

    # LLM settings — compatible with any OpenAI-format API endpoint
    llm_base_url: str = "https://api.xiaomi.com/v1"
    llm_api_key: str = ""
    llm_model: str = "MiMo"
    llm_max_tokens: int = 4096
    llm_temperature: float = 0.3
    llm_timeout_seconds: int = 120

    model_config = SettingsConfigDict(env_file=str(_ENV_FILE), env_file_encoding="utf-8", extra="ignore")


settings = Settings()
