from fastapi import APIRouter, Request, HTTPException
from ..clients.auth_client import AuthClient
from ..resilience.circuit_breaker import CircuitBreaker

router = APIRouter(prefix="/auth", tags=["Auth"])
client = AuthClient()
breaker = CircuitBreaker()


@router.get("/verify")
async def verify_user(request: Request):
    """
    Verifica el token JWT de la petición y retorna los datos del usuario.
    inputs:
        request: Objeto Request de FastAPI.
    outputs:
        dict: Datos del usuario verificado.
    """

    token = request.headers.get("Authorization")

    if not breaker.can_execute("auth_service"):
        raise HTTPException(status_code=503, detail="Auth service unavailable")

    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        return await client.verify_token(
            token.replace("Bearer ", ""),
            headers={"X-Request-ID": request.state.request_id},
        )

        breaker.record_success("auth_service")
    except Exception:
        breaker.record_failure("auth_service")
        raise HTTPException(status_code=401, detail="Invalid token")
