from pydantic_settings import BaseSettings
import os
import dotenv

dotenv.load_dotenv()


class Settings(BaseSettings):
    """
    Configuración central del Gateway.
    Actúa como punto único de configuración (Singleton lógico).
    """
    ENV: str = "development"
    API_VERSION: str = "v1"
    SERVICE_NAME: str = "gateway-service"
    HOST: str = "localhost"
    PORT: int = 8000
    MASTER_USERNAME: str = "masteruser"
    MASTER_PASSWORD: str = "masterpassword"
    MASTER_API_KEY: str = "supersecretmasterkey"
    LOG_LEVEL: str = "INFO"
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL",
                                      "http://localhost:8001")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
