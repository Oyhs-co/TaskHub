from fastapi import HTTPException
from typing import Dict, Any, Literal
from ..utils.supabase import supabase_client
from ..utils.user import UserIdentity


class AuthService:
    """
    Orquesta login, registro y validación de identidad.
    """

    def register(self, email: str, password: str) -> UserIdentity:
        try:
            response = supabase_client.auth().sign_up({
                "email": email,
                "password": password,
            })

            if response.user is None:
                raise ValueError("Supabase did not return a user")

            if response.user.email is None:
                raise ValueError("Supabase did not return a user email")

            self._create_guide_project(response.user.id)

            return UserIdentity(
                user_id=response.user.id,
                email=response.user.email,
                is_new=True,
            )

        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail="Unexpected error during registration",
            ) from exc

    def login(self, email: str, password: str) -> Dict[str, Any]:
        try:
            response = supabase_client.auth().sign_in_with_password({
                "email": email,
                "password": password,
            })

            if response.session is None:
                raise ValueError("Invalid credentials")

            return {
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
            }

        except ValueError as exc:
            raise HTTPException(status_code=401, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail="Unexpected error during login",
            ) from exc

    def login_with_oauth(self,
                         provider: Literal["google", "github"],
                         redirect_to: str) -> Dict[str, Any]:
        """
        Inicia el flujo OAuth con el proveedor indicado.
        Ejemplos de provider: google, github, discord, azure, etc.
        """
        try:
            response = supabase_client.auth().sign_in_with_oauth({
                    "provider": provider,
                    "options": {
                        "redirect_to": redirect_to,
                    },
                })

            if not response or not response.url:
                raise ValueError("OAuth URL was not generated")

            return {
                "provider": provider,
                "auth_url": response.url,
            }

        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail="Unexpected error during OAuth login",
            ) from exc

    def verify(self, token: str) -> dict:
        """
        Verifica la validez del token JWT y extrae la información del usuario.

        inputs:
            token: Token JWT a verificar.
        outputs:
            dict: Datos del usuario verificado.
        """
        try:
            user = supabase_client.auth().get_user(token).user

            if not user:
                raise HTTPException(status_code=401, detail="Invalid token")

            return {
                "user_id": user.id,
                "email": user.email,
                "email_verified": user.email_confirmed_at is not None,
                "onboarding_completed": False,  # luego DB propia
                "roles": ["user"],
            }

        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail="Unexpected error during token verification",
            ) from exc

    def _create_guide_project(self, user_id: str) -> None:
        """
        Rama preparada para onboarding:
        Genera un proyecto guía al crear un usuario.
        """
        pass


auth_service = AuthService()
