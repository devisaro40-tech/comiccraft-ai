from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    debug: bool = True
    gemini_api_key: str = ""

    gemini_outline_model: str = "gemini-2.0-flash"
    gemini_story_model: str = "gemini-2.5-pro"

    image_model: str = "stabilityai/stable-diffusion-xl-base-1.0"
    image_provider: str = "auto"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()