from typing import Dict, Optional, Any
from pydantic import BaseModel


class TokenPayload(BaseModel):
    """
    Representa la información relevante extraída del JWT.
    """

    def __init__(self, payload: Dict[str, str | Any]):
        self.user_id: str | Any = payload.get("sub")
        self.email: Optional[str] = payload.get("email")
        self.provider: Optional[str] = payload.get("provider")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "provider": self.provider,
        }


def extract_bearer_token(authorization_header: str) -> str:
    """
    Extrae el token Bearer del encabezado de autorización.
    """
    try:
        scheme, token = authorization_header.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid authorization scheme")
        return token
    except ValueError:
        raise ValueError("Invalid authorization header format")
