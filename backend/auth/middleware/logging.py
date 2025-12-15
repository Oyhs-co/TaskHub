from starlette.middleware.base import BaseHTTPMiddleware
import time
from fastapi import Request
from logging import Logger


class ServiceLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para registrar información de
    cada petición HTTP con nombre de servicio.
    """

    def __init__(self, app, logger: Logger, service_name: str):
        super().__init__(app)
        self.logger = logger
        self.service_name = service_name

    async def dispatch(self, request: Request, call_next):
        """
        Registra el inicio y fin de cada petición HTTP.
        inputs:
            request: Objeto Request de FastAPI.
            call_next: Función para continuar con la cadena de middlewares.
        outputs:
            response: Objeto Response de FastAPI.
        """
        start_time = time.time()

        request_id = request.headers.get("X-Request-ID")

        response = await call_next(request)

        duration = int((time.time() - start_time) * 1000)

        self.logger.info(
            "request_completed",
            extra={
                "extra": {
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": duration,
                }
            },
        )

        return response
