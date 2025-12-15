from fastapi import FastAPI
from .log.logger import get_logger
from .middleware.logging import LoggingMiddleware
from .middleware.master_user import MasterUserMiddleware
from fastapi.middleware.cors import CORSMiddleware
from .middleware.auth_requiried import AuthRequiredMiddleware
from .routers import auth
logger = get_logger("api-gateway")

app = FastAPI(title="TaskHub API Gateway")

app.add_middleware(LoggingMiddleware, logger=logger)
app.add_middleware(MasterUserMiddleware)
app.add_middleware(AuthRequiredMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/debug")
def debug_info():
    try:
        return {"debug": "This is debug information",
                "service": "API Gateway",
                "version": "1.0.0",
                }
    except Exception as exc:
        return {"error": str(exc)}


@app.get("/health")
def health_check():
    try:
        return {"status": "healthy"}
    except Exception as exc:
        return {"status": "unhealthy", "error": str(exc)}


@app.get("/")
def read_root():
    try:
        return {"message": "API Gateway is running"}
    except Exception as exc:
        return {"error": str(exc)}
