"""Application configuration via Pydantic Settings."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API
    anthropic_api_key: str = ""

    # Database
    db_path: Path = Path("./cert_pepper.db")

    # Content root (path to security-plus repo root)
    content_root: Path = Path("..")

    # AI models
    haiku_model: str = "claude-haiku-4-5-20251001"
    sonnet_model: str = "claude-sonnet-4-6"

    # Study settings
    default_session_size: int = 10
    mastery_threshold: float = 0.85

    @property
    def db_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.db_path}"

    @property
    def questions_dir(self) -> Path:
        return self.content_root / "practice-questions"

    @property
    def flashcards_path(self) -> Path:
        return self.content_root / "flashcards" / "key-concepts.md"

    @property
    def acronyms_path(self) -> Path:
        return self.content_root / "acronyms.md"

    @property
    def domains_dir(self) -> Path:
        return self.content_root / "domains"


def get_settings() -> Settings:
    return Settings()
