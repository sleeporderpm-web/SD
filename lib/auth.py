import json
import os
from typing import Dict, Optional
from pathlib import Path

from passlib.hash import pbkdf2_sha256


# Local file storage for users (development mode)
USERS_FILE = Path(__file__).parent.parent / ".data" / "users.json"


def _ensure_users_json():
    """Ensure users.json file exists."""
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not USERS_FILE.exists():
        with open(USERS_FILE, "w") as f:
            json.dump({"users": {}}, f)


def _load() -> Dict[str, Dict[str, str]]:
    """Load users from local JSON file."""
    _ensure_users_json()
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def _save(data: Dict[str, Dict[str, str]]):
    """Save users to local JSON file."""
    _ensure_users_json()
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def register(email: str, password: str) -> bool:
    """Register a new user with email and hashed password."""
    email = email.strip().lower()
    data = _load()
    if email in data["users"]:
        return False
    hashed = pbkdf2_sha256.hash(password)
    data["users"][email] = hashed
    _save(data)
    return True


def verify(email: str, password: str) -> bool:
    """Verify user credentials."""
    email = email.strip().lower()
    data = _load()
    hashed = data["users"].get(email)
    if not hashed:
        return False
    return pbkdf2_sha256.verify(password, hashed)


def get_user(email: str) -> Optional[str]:
    """Get user by email."""
    email = email.strip().lower()
    data = _load()
    return data["users"].get(email)
