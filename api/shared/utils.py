from supabase import create_client
from config import settings

def get_supabase_client(user_token: str):
    client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    client.auth.set_session(user_token)
    return client