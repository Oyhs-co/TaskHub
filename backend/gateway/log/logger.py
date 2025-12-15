import logging
import json
import sys
from datetime import datetime


class JsonFormatter(logging.Formatter):
    """
    Formateador de logs en formato JSON.
    """
    def format(self, record: logging.LogRecord) -> str:
        """
        Formatea el registro de log como una cadena JSON.

        inputs:
            record: Registro de log
        outputs:
            str: Registro formateado en JSON
        """
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "service": record.name,
            "message": record.getMessage(),
        }

        if hasattr(record, "extra"):
            payload.update(record.extra)

        return json.dumps(payload)


def get_logger(service_name: str) -> logging.Logger:
    """
    Obtiene un logger configurado para el servicio dado.

    inputs:
        service_name: Nombre del servicio
    outputs:
        logger: Logger configurado
    example:
        logger = get_logger("gateway-service")
    """
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    if not logger.handlers:
        logger.addHandler(handler)

    logger.propagate = False
    return logger
