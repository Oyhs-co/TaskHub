from jose import JWTError, jwt
from fastapi import HTTPException
from typing import Dict, Any
from ..config import settings
from ..utils.token import TokenPayload


class JWTService:
    """
    Servicio encargado exclusivamente de validar tokens JWT.
    """

    def __init__(self, secret: str, algorithm: str, audience: str):
        self._secret = secret
        self._algorithm = algorithm
        self._audience = audience

    def validate_token(self, token: str) -> TokenPayload:
        payload = self._decode_token(token)
        return TokenPayload(payload)

    def _decode_token(self, token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(
                token,
                self._secret,
                algorithms=[self._algorithm],
                audience=self._audience,
            )
        except JWTError:
            raise HTTPException(status_code=401,
                                detail="Invalid or expired token")


jwt_service = JWTService(
    settings.SUPABASE_JWT_SECRET,
    settings.SUPABASE_JWT_ALGORITHM,
    settings.SUPABASE_JWT_AUDIENCE,
)
