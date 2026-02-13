import json
from typing import Dict, Optional

from passlib.hash import pbkdf2_sha256

from .db import get_client


BUCKET = "appdata"
KEY_PATH = "users.json"


def _ensure_users_json():
    client = get_client()
    try:
        client.storage.from_(BUCKET).download(KEY_PATH)
    except Exception:
        content = json.dumps({"users": {}}).encode("utf-8")
        try:
            client.storage.from_(BUCKET).upload(KEY_PATH, content, {"content-type": "application/json"})
        except Exception:
            pass


def _load() -> Dict[str, Dict[str, str]]:
    client = get_client()
    _ensure_users_json()
    raw = client.storage.from_(BUCKET).download(KEY_PATH)
    data = json.loads(raw.decode("utf-8"))
    return data


def _save(data: Dict[str, Dict[str, str]]):
    client = get_client()
    payload = json.dumps(data).encode("utf-8")
    client.storage.from_(BUCKET).update(KEY_PATH, payload, {"content-type": "application/json"})


def register(email: str, password: str) -> bool:
    email = email.strip().lower()
    data = _load()
    if email in data["users"]:
        return False
    hashed = pbkdf2_sha256.hash(password)
    data["users"][email] = hashed
    _save(data)
    return True


def verify(email: str, password: str) -> bool:
    email = email.strip().lower()
    data = _load()
    hashed = data["users"].get(email)
    if not hashed:
        return False
    return pbkdf2_sha256.verify(password, hashed)


def get_user(email: str) -> Optional[str]:
    email = email.strip().lower()
    data = _load()
    return data["users"].get(email)
