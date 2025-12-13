from fastapi import APIRouter, Header
from .service import auth_service
from ..utils.token import extract_bearer_token
from typing import Literal
import logging as log

log.getLogger("auth-service").info("Cargando rutas del AuthService")

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register")
def register(email: str, password: str):
    return auth_service.register(email, password).to_dict()


log.getLogger("auth-service").info("Ruta /register cargada")


@auth_router.post("/login")
def login(email: str, password: str):
    return auth_service.login(email, password)


log.getLogger("auth-service").info("Ruta /login cargada")


@auth_router.post("/login/oauth")
def login_oauth(provider: Literal["google", "github"], redirect_to: str):
    return auth_service.login_with_oauth(provider, redirect_to)


log.getLogger("auth-service").info("Ruta /login/oauth cargada")


@auth_router.get("/validate")
def validate_token(authorization: str = Header(...)):
    token = extract_bearer_token(authorization)
    return auth_service.validate(token).to_dict()


log.getLogger("auth-service").info("Ruta /validate cargada")
