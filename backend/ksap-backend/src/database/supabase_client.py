import os
from supabase import create_client, Client
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class SupabaseClient:
    """Supabase client wrapper for KSAP platform"""
    
    def __init__(self):
        self.url: str = os.environ.get("SUPABASE_URL", "")
        self.key: str = os.environ.get("SUPABASE_ANON_KEY", "")
        self.service_key: str = os.environ.get("SUPABASE_SERVICE_KEY", "")
        self._client: Optional[Client] = None
        self._admin_client: Optional[Client] = None
    
    @property
    def client(self) -> Client:
        """Get Supabase client with anon key (for frontend operations)"""
        if not self._client:
            if not self.url or not self.key:
                raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")
            self._client = create_client(self.url, self.key)
        return self._client
    
    @property
    def admin_client(self) -> Client:
        """Get Supabase client with service key (for admin operations)"""
        if not self._admin_client:
            if not self.url or not self.service_key:
                raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
            self._admin_client = create_client(self.url, self.service_key)
        return self._admin_client
    
    def test_connection(self) -> bool:
        """Test connection to Supabase"""
        try:
            # Try to fetch from a system table
            response = self.client.from_("information_schema.tables").select("table_name").limit(1).execute()
            return response.data is not None
        except Exception as e:
            logger.error(f"Supabase connection test failed: {e}")
            return False

# Global instance
supabase_client = SupabaseClient()

# Convenience functions
def get_supabase() -> Client:
    """Get the main Supabase client"""
    return supabase_client.client

def get_admin_supabase() -> Client:
    """Get the admin Supabase client"""
    return supabase_client.admin_client

