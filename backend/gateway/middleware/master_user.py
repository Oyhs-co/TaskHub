from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from ..config import settings


class MasterUserMiddleware(BaseHTTPMiddleware):
    """
    Middleware para autenticar peticiones con una clave maestra.
    Si la clave es válida, asigna un usuario "master" con rol "superuser".
    """
    async def dispatch(self, request: Request, call_next):
        """
        Verifica la clave maestra en las cabeceras de la petición.
        Si es válida, asigna el usuario master al estado de la petición.

        inputs:
            request: Objeto Request de FastAPI.
            call_next: Función para continuar con la cadena de middlewares.
        outputs:
            response: Objeto Response de FastAPI.
        """
        api_key = request.headers.get("X-Master-Key")

        if api_key:
            if api_key != settings.MASTER_API_KEY:
                raise HTTPException(status_code=401,
                                    detail="Invalid master key")

            request.state.user = {
                "user_id": "master",
                "role": "superuser",
            }

        return await call_next(request)
