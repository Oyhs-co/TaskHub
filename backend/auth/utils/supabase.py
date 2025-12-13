from supabase import create_client, Client
from ..config import settings


class SupabaseClient:
    """
    Cliente centralizado de Supabase.
    Usa service_role para operaciones privilegiadas (backend-onlyn).
    """

    def __init__(self, url: str, service_key: str):
        self._client: Client = create_client(url, service_key)

    def auth(self):
        return self._client.auth

    def db(self):
        return self._client


supabase_client = SupabaseClient(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_ROLE,
)
