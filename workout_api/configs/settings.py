from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://workout:workout@localhost:5432/workout"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()