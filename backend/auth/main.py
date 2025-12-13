from fastapi import FastAPI
from backend.auth.routers.auth_router import auth_router

app = FastAPI(title="Auth Service",
              version="1.0.0",
              description="Servicio de autenticación para TaskHub"
              )

app.include_router(auth_router)


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
    uvicorn.run(app, host="0.0.0.0", port=8000)
