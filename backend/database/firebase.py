import os
import json
import time
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
import requests

# Load environment variables strictly from .env file
try:
    from dotenv import load_dotenv
    backend_env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    root_env = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
    if os.path.exists(backend_env):
        load_dotenv(backend_env)
    elif os.path.exists(root_env):
        load_dotenv(root_env)
except ImportError:
    pass

# Retrieve Firebase URL strictly from environment (.env)
FIREBASE_DATABASE_URL = os.environ.get(
    "FIREBASE_DATABASE_URL", 
    "https://tcm-nlp-default-rtdb.asia-southeast1.firebasedatabase.app"
).rstrip("/")

def get_auth_param() -> str:
    """Helper to return auth query param if secret is configured."""
    secret = (
        os.environ.get("FIREBASE_AUTH_SECRET") or 
        os.environ.get("FIREBASE_DATABASE_SECRET") or 
        ""
    )
    return f"?auth={secret}" if secret else ""

def init_firebase():
    """Verify live connection to Firebase Realtime Database."""
    db_url = os.environ.get("FIREBASE_DATABASE_URL", FIREBASE_DATABASE_URL).rstrip("/")
    auth_param = get_auth_param()
    try:
        url = f"{db_url}/.json{auth_param}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            print(f"[Firebase] Connected to Realtime Database via REST: {db_url}")
        else:
            print(f"[Firebase] Realtime Database status {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"[Firebase] Realtime Database connection error: {e}")

def get_user_comments_for_post(post_id: int) -> List[Dict[str, Any]]:
    """
    Fetch approved comments for a specific post DIRECTLY from Firebase Realtime Database.
    No local database or in-memory cache is used.
    If comments are deleted in Firebase, they disappear immediately here.
    """
    db_url = os.environ.get("FIREBASE_DATABASE_URL", FIREBASE_DATABASE_URL).rstrip("/")
    if not db_url:
        return []

    auth_param = get_auth_param()
    url = f"{db_url}/comments.json{auth_param}"

    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if not data or not isinstance(data, dict):
                return []

            approved = []
            for c in data.values():
                if (
                    isinstance(c, dict)
                    and int(c.get("post_id", 0)) == post_id
                    and c.get("status") == "approved"
                ):
                    approved.append(c)

            approved.sort(key=lambda x: x.get("id", 0))
            return approved
        else:
            print(f"[Firebase RTDB] Fetch error status {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"[Firebase RTDB] Fetch exception: {e}")

    return []

def get_all_approved_comments() -> Dict[int, List[Dict[str, Any]]]:
    """
    Fetch all approved comments from Firebase Realtime Database in a single call,
    grouped by post_id.
    """
    db_url = os.environ.get("FIREBASE_DATABASE_URL", FIREBASE_DATABASE_URL).rstrip("/")
    if not db_url:
        return {}

    auth_param = get_auth_param()
    url = f"{db_url}/comments.json{auth_param}"

    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if not data or not isinstance(data, dict):
                return {}

            by_post: Dict[int, List[Dict[str, Any]]] = {}
            for c in data.values():
                if isinstance(c, dict) and c.get("status") == "approved":
                    pid = int(c.get("post_id", 0))
                    if pid not in by_post:
                        by_post[pid] = []
                    by_post[pid].append(c)

            for pid in by_post:
                by_post[pid].sort(key=lambda x: x.get("id", 0))
            return by_post
    except Exception as e:
        print(f"[Firebase RTDB] Fetch all error: {e}")

    return {}

def count_user_comments_for_post(post_id: int) -> int:
    """Count comments directly from Firebase Realtime Database."""
    return len(get_user_comments_for_post(post_id))

def save_comment_to_firebase(
    post_id: int,
    username: str,
    comment_text: str,
    toxicity_probability: float,
    status: str
) -> Dict[str, Any]:
    """
    Save comment strictly to Firebase Realtime Database.
    No other database is used.
    """
    comment_id = int(time.time() * 1000)
    now_iso = datetime.now(timezone.utc).isoformat()
    comment_record = {
        "id": comment_id,
        "post_id": post_id,
        "username": username,
        "comment_text": comment_text,
        "toxicity_probability": toxicity_probability,
        "status": status,
        "created_at": now_iso
    }

    db_url = os.environ.get("FIREBASE_DATABASE_URL", FIREBASE_DATABASE_URL).rstrip("/")
    auth_param = get_auth_param()

    if db_url:
        try:
            write_url = f"{db_url}/comments/{comment_id}.json{auth_param}"
            resp = requests.put(write_url, json=comment_record, timeout=5)
            if resp.status_code == 200:
                print(f"✅ [Firebase RTDB] Comment {comment_id} written to Firebase.")
            else:
                print(f"⚠️ [Firebase RTDB Status {resp.status_code}]: {resp.text}")
        except Exception as e:
            print(f"⚠️ [Firebase RTDB Connection Error]: {e}")

    return comment_record
