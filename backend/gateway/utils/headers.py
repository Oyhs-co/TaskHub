from fastapi import Request


def get_request_headers(request: Request) -> dict:
    """
    Obtiene las cabeceras relevantes de la petición HTTP.

    inputs:
        request: Objeto Request de FastAPI.
    outputs:
        dict: Diccionario con las cabeceras relevantes.
    """
    return {
        "X-Request-ID": request.state.request_id,
    }
