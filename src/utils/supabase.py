from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

def get_supabase_client():
    """
    獲取 Supabase 客戶端實例
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
    
    return create_client(SUPABASE_URL, SUPABASE_KEY)