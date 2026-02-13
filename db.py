import os
from typing import Any, Dict, List, Optional

try:
    import streamlit as st
except Exception:
    st = None

from supabase import create_client, Client

_client: Optional[Client] = None


def get_client() -> Client:
    global _client
    if _client:
        return _client
    url = None
    key = None
    if st is not None:
        try:
            url = st.secrets.get("SUPABASE_URL")
            key = st.secrets.get("SUPABASE_KEY")
        except Exception:
            pass
    url = url or os.environ.get("SUPABASE_URL")
    key = key or os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Missing Supabase credentials")
    _client = create_client(url, key)
    return _client


def save_analysis(row: Dict[str, Any]) -> Dict[str, Any]:
    client = get_client()
    res = client.table("analyses").insert(row).execute()
    return res.data[0] if res.data else {}


def list_user_analyses(email: str, limit: int = 50) -> List[Dict[str, Any]]:
    client = get_client()
    res = (
        client.table("analyses")
        .select("*")
        .eq("user_email", email)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return res.data or []


def list_all_analyses(limit: int = 200) -> List[Dict[str, Any]]:
    client = get_client()
    res = client.table("analyses").select("*").order("created_at", desc=True).limit(limit).execute()
    return res.data or []


def get_analysis_by_id(analysis_id: str) -> Optional[Dict[str, Any]]:
    client = get_client()
    res = client.table("analyses").select("*").eq("id", analysis_id).limit(1).execute()
    rows = res.data or []
    return rows[0] if rows else None
