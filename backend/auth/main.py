from fastapi import FastAPI
from .routers.auth_router import auth_router
from .log.logger import get_logger
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
from .middleware.logging import ServiceLoggingMiddleware

logger = get_logger(settings.SERVICE_NAME)

app = FastAPI(title="Auth Service",
              version="1.0.0",
              description="Servicio de autenticación para TaskHub"
              )

app.add_middleware(ServiceLoggingMiddleware,
                   logger=logger,
                   service_name=settings.SERVICE_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)

app.version = settings.API_VERSION


@app.get("/")
def read_root():
    try:
        return {"message": "Auth Service is running"}
    except Exception as exc:
        return {"error": str(exc)}


@app.get("/health")
def health_check():
    try:
        return {"status": "healthy"}
    except Exception as exc:
        return {"status": "unhealthy", "error": str(exc)}


@app.get("/debug")
def debug_info():
    try:
        return {"debug": "This is debug information",
                "service": "Auth Service",
                "version": "1.0.0",
                }
    except Exception as exc:
        return {"error": str(exc)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
