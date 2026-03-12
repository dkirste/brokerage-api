from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_KEY: str = "test-key"
    FMCSA_API_KEY: str = ""
    DATABASE_URL: str = "postgresql+asyncpg://brokerage:brokerage_secret@db:5432/brokerage"

    model_config = {"env_file": ".env"}


settings = Settings()
