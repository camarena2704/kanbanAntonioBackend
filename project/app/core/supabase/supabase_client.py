import os

from supabase._async.client import AsyncClient, create_client

# Environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

# Cached clients (Singleton)
_supabase_anon: AsyncClient = None
_supabase_admin: AsyncClient = None


async def get_supabase() -> AsyncClient:
    """
    Returns the public Supabase client (using ANON key).
    Use this for operations like login, registration, etc.
    Implements singleton pattern.
    """
    global _supabase_anon
    if _supabase_anon is None:
        if not SUPABASE_URL or not SUPABASE_ANON_KEY:
            raise RuntimeError("SUPABASE_URL or SUPABASE_ANON_KEY not configured")
        _supabase_anon = await create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    return _supabase_anon


async def get_supabase_admin() -> AsyncClient:
    """
    Returns the admin Supabase client (using SERVICE_ROLE key).
    Use this for privileged operations like deleting users.
    Implements singleton pattern.
    """
    global _supabase_admin
    if _supabase_admin is None:
        if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
            raise RuntimeError(
                "SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not configured"
            )
        _supabase_admin = await create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    return _supabase_admin
