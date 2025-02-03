from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    roboflow_api_key: str
    huggingface_token: str
    wandb_api_key: str
    
    model_config = SettingsConfigDict(env_file=".env")


def get_settings() -> Settings:
    return Settings()
