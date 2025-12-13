"""
Logger central reutilizable para microservicios TaskHub.
Diseñado para FastAPI, Docker y entornos dev/prod.
"""

import logging
import sys
from typing import Optional


def setup_logging(
    service_name: str,
    level: str = "INFO",
    log_to_file: bool = False,
    file_path: Optional[str] = None,
) -> None:
    """
    Configura el logging global del microservicio.

    Parameters
    ----------
    service_name : str
        Nombre del microservicio (ej: "auth-service")
    level : str
        Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    log_to_file : bool
        Si True, también escribe logs a archivo
    file_path : Optional[str]
        Ruta del archivo de logs
    """

    log_level = getattr(logging, level.upper(), logging.INFO)

    handlers = [logging.StreamHandler(sys.stdout)]

    if log_to_file and file_path:
        handlers.append(logging.FileHandler(file_path))

    logging.basicConfig(
        level=log_level,
        format=(
            "%(asctime)s | %(levelname)s | %(name)s | "
            "%(filename)s:%(lineno)d | %(message)s"
        ),
        handlers=handlers,
    )

    logging.getLogger("uvicorn").setLevel(log_level)
    logging.getLogger("uvicorn.error").setLevel(log_level)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    logging.getLogger(service_name).info("Logger inicializado")


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger con nombre consistente.

    Parameters
    ----------
    name : str
        Nombre del módulo o componente

    Returns
    -------
    logging.Logger
    """

    return logging.getLogger(name)
