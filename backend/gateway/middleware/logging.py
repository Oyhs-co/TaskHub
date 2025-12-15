import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from logging import Logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para registrar información de cada petición HTTP.
    """
    def __init__(self, app, logger: Logger):
        super().__init__(app)
        self.logger = logger

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

        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        response = await call_next(request)

        duration_ms = int((time.time() - start_time) * 1000)

        user = getattr(request.state, "user", {})
        user_id = user.get("user_id")

        self.logger.info(
            "request_completed",
            extra={
                "extra": {
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                    "user_id": user_id,
                }
            },
        )

        response.headers["X-Request-ID"] = request_id
        return response
