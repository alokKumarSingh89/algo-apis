from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MODE: str


settings = Settings()