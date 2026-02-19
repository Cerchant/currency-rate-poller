from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/currency_db"
    poll_interval_minutes: int = 10
    base: str = "USD"
    symbols: str = "EUR,RUB"
    http_timeout_seconds: int = 5
    log_level: str = "INFO"

    @property
    def symbols_list(self) -> list[str]:
        return [s.strip() for s in self.symbols.split(",") if s.strip()]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
