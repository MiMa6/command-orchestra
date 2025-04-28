from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    OBSIDIAN_EXERCISE_VAULT_PATH: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


# Singleton pattern for settings
_settings = None


def get_settings():
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
