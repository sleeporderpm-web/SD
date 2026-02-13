import os
import json
import uuid
from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime

try:
    import streamlit as st
except Exception:
    st = None

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None

_client: Optional[Client] = None

# Local file storage for analyses (fallback when Supabase unavailable)
DATA_DIR = Path(__file__).parent.parent / ".data"
ANALYSES_FILE = DATA_DIR / "analyses.json"


def _ensure_local_storage():
    """Ensure local data directory and files exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not ANALYSES_FILE.exists():
        with open(ANALYSES_FILE, "w") as f:
            json.dump({"analyses": []}, f)


def _load_local_analyses() -> List[Dict[str, Any]]:
    """Load analyses from local JSON file."""
    _ensure_local_storage()
    with open(ANALYSES_FILE, "r") as f:
        return json.load(f).get("analyses", [])


def _save_local_analyses(analyses: List[Dict[str, Any]]):
    """Save analyses to local JSON file."""
    _ensure_local_storage()
    with open(ANALYSES_FILE, "w") as f:
        json.dump({"analyses": analyses}, f, indent=2)


def get_client() -> Optional[Client]:
    """Initialize and return Supabase client if available."""
    global _client
    if _client:
        return _client
    
    if not SUPABASE_AVAILABLE:
        return None
    
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
        return None
    
    try:
        _client = create_client(url, key)
        return _client
    except Exception:
        return None


def save_analysis(row: Dict[str, Any]) -> Dict[str, Any]:
    """Save a sleep analysis record to the database (Supabase or local)."""
    client = get_client()
    
    # Ensure ID and timestamp
    if "id" not in row:
        row["id"] = str(uuid.uuid4())
    if "created_at" not in row:
        row["created_at"] = datetime.now().isoformat()
    
    if client:
        try:
            res = client.table("analyses").insert(row).execute()
            return res.data[0] if res.data else row
        except Exception as e:
            # Fallback to local storage if Supabase fails
            pass
    
    # Use local storage
    analyses = _load_local_analyses()
    analyses.append(row)
    _save_local_analyses(analyses)
    return row


def list_user_analyses(email: str, limit: int = 50) -> List[Dict[str, Any]]:
    """List all analyses for a specific user."""
    client = get_client()
    
    if client:
        try:
            res = (
                client.table("analyses")
                .select("*")
                .eq("user_email", email)
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            return res.data or []
        except Exception:
            pass
    
    # Use local storage
    analyses = _load_local_analyses()
    user_analyses = [a for a in analyses if a.get("user_email") == email]
    user_analyses.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return user_analyses[:limit]


def list_all_analyses(limit: int = 200) -> List[Dict[str, Any]]:
    """List all analyses (admin view)."""
    client = get_client()
    
    if client:
        try:
            res = client.table("analyses").select("*").order("created_at", desc=True).limit(limit).execute()
            return res.data or []
        except Exception:
            pass
    
    # Use local storage
    analyses = _load_local_analyses()
    analyses.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return analyses[:limit]


def get_analysis_by_id(analysis_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific analysis by ID."""
    client = get_client()
    
    if client:
        try:
            res = client.table("analyses").select("*").eq("id", analysis_id).limit(1).execute()
            rows = res.data or []
            return rows[0] if rows else None
        except Exception:
            pass
    
    # Use local storage
    analyses = _load_local_analyses()
    for analysis in analyses:
        if analysis.get("id") == analysis_id:
            return analysis
    return None

