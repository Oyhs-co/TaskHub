import httpx
from ..config import settings


class AuthClient:
    def __init__(self):
        self.base_url = settings.AUTH_SERVICE_URL

    async def verify_token(self, token: str, headers: dict):
        """
        Verifica un token JWT con el servicio de autenticación.

        inputs:
            token: Token JWT a verificar.
            headers: Cabeceras adicionales para la petición.
        outputs:
            dict: Datos del usuario verificado.
        """
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{self.base_url}/auth/verify",
                headers={
                    "Authorization": f"Bearer {token}",
                    **headers,
                },
            )
            response.raise_for_status()
            return response.json()
