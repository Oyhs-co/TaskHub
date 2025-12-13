import os
import dotenv
import logging as log
from ..core.logging import setup_logging

dotenv.load_dotenv()

setup_logging(service_name="auth-service",
              level=os.getenv("LOG_LEVEL", "INFO"),
              log_to_file=os.getenv("LOG_TO_FILE", "False") == "True",
              file_path=os.getenv("LOG_FILE_PATH", "auth_service.log"))


class Settings:
    """
    Configuración central del AuthService.
    Actúa como punto único de configuración (Singleton lógico).
    """

    log.getLogger("auth-service").info(
        "Cargando configuración del AuthService")

    try:
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
    except Exception as e:
        log.getLogger("auth-service").error(
            f"Error cargando configuración: {e}")
        raise e


settings = Settings()
