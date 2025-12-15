import os
import dotenv
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class Settings(BaseSettings):
    """
    Configuración central del AuthService.
    Actúa como punto único de configuración (Singleton lógico).
    """

    try:
        ENV: str = "development"
        API_VERSION: str = "v1"
        SERVICE_NAME: str = "auth-service"
        HOST: str = os.getenv("HOST", "localhost")
        PORT: int = int(os.getenv("PORT", 8001))
        SUPABASE_URL: str = os.getenv("SUPABASE_URL",
                                      "https://your-supabase-url.supabase.co")
        SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY",
                                           "YOUR_ANON_KEY")
        SUPABASE_SERVICE_ROLE: str = os.getenv("SUPABASE_SERVICE_ROLE",
                                               "YOUR_SERVICE_ROLE_KEY")
        SUPABASE_JWT_SECRET: str = os.getenv("SUPABASE_JWT_SECRET",
                                             "YOUR_JWT_SECRET")
        SUPABASE_JWT_ALGORITHM: str = os.getenv("SUPABASE_JWT_ALGORITHM",
                                                "HS256")
        SUPABASE_JWT_AUDIENCE: str = os.getenv("SUPABASE_JWT_AUDIENCE",
                                               "authenticated")
        LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"

    except Exception as e:
        raise e


settings = Settings()
