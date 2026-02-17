from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # SPACY_MODEL: str = "en_core_web_sm"
    SPACY_MODEL: str = "en_core_web_trf"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "OCR Service"
    GEMINI_API_KEY: str = ""

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
