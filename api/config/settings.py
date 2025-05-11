from pydantic_settings import BaseSettings, SettingsConfigDict
from supabase import create_client

class Settings(BaseSettings):
    DATABASE_URL: str
    SUPABASE_URL: str
    SUPABASE_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
settings = Settings()

# Use for global operations in subapase (Ex: Registering a user)
global_supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)