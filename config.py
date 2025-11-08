from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(extra='ignore')

    llm_api_key: str
    llm_model: str

    weater_api_key: str


settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8"
)