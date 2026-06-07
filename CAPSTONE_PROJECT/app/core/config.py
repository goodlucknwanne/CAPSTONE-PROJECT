from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
        env_file_encoding = "utf-8"


settings = Settings()