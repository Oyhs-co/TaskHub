from typing import Dict, Any


class UserIdentity:
    """
    Modelo de dominio que representa un usuario autenticado.
    """

    def __init__(self, user_id: str, email: str, is_new: bool = False):
        self.user_id = user_id
        self.email = email
        self.is_new = is_new

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "is_new": self.is_new,
        }
