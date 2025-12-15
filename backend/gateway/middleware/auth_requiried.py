from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from ..clients.auth_client import AuthClient

auth_client = AuthClient()


class AuthRequiredMiddleware(BaseHTTPMiddleware):

    PUBLIC_PATHS = ("/auth/register",
                    "/auth/login",
                    "/auth/login/oauth",
                    "/health",
                    "/docs",
                    "/debug",
                    "/openapi.json",
                    "/auth",
                    "/")

    async def dispatch(self, request: Request, call_next):

        """
        Middleware para requerir autenticación en las rutas protegidas.
        inputs:
            request: Objeto Request de FastAPI.
            call_next: Función para continuar con la cadena de middlewares.
        outputs:
            response: Objeto Response de FastAPI.
        """

        # Rutas públicas
        if request.url.path.startswith(self.PUBLIC_PATHS):
            return await call_next(request)

        # Usuario maestro ya validado
        if hasattr(request.state, "user"):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401,
                                detail="Authorization required")

        token = auth_header.replace("Bearer ", "")

        try:
            user = await auth_client.verify_token(
                token,
                headers={"X-Request-ID": request.state.request_id},
            )
            request.state.user = user

        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await call_next(request)
