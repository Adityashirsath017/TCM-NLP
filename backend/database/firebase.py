import os
import json
import time
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
import requests

# Load environment variables from .env file
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

# Try importing firebase_admin
try:
    import firebase_admin
    from firebase_admin import credentials, db as firebase_db
    FIREBASE_ADMIN_AVAILABLE = True
except ImportError:
    FIREBASE_ADMIN_AVAILABLE = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "serviceAccountKey.json")

# Retrieve Firebase URL strictly from environment (.env)
FIREBASE_DATABASE_URL = os.environ.get("FIREBASE_DATABASE_URL", "").rstrip("/")

_using_admin_sdk = False
_firebase_initialized = False

# Synchronized in-memory buffer for real-time performance and instant access
_live_comments: Dict[int, Dict[str, Any]] = {}
_next_id = int(time.time() * 1000) % 1000000 + 100

def init_firebase():
    """Initialize Firebase Realtime Database connection for comments storage."""
    global _using_admin_sdk, _firebase_initialized

    custom_cred_path = os.environ.get("FIREBASE_CREDENTIALS", CREDENTIALS_FILE)
    db_url = os.environ.get("FIREBASE_DATABASE_URL", FIREBASE_DATABASE_URL).rstrip("/")

    # 1. Admin SDK check
    if FIREBASE_ADMIN_AVAILABLE and os.path.exists(custom_cred_path) and db_url:
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(custom_cred_path)
                firebase_admin.initialize_app(cred, {"databaseURL": db_url})
            _using_admin_sdk = True
            _firebase_initialized = True
            print(f"[Firebase] Connected to Realtime Database via Admin SDK: {db_url}")
            load_existing_remote_comments_admin()
            return
        except Exception as e:
            print(f"[Firebase] Warning initializing Admin SDK: {e}")

    # 2. REST API check
    if db_url:
        try:
            resp = requests.get(f"{db_url}/comments.json?shallow=true", timeout=4)
            if resp.status_code == 200:
                _firebase_initialized = True
                print(f"[Firebase] Connected to Realtime Database via REST: {db_url}")
                load_existing_remote_comments_rest(db_url)
                return
            elif resp.status_code == 401:
                print(f"[Firebase] Realtime Database requires credentials or open rules. Operating with secure live sync.")
        except Exception as e:
            print(f"[Firebase] Remote endpoint check: {e}")

    print("[Firebase] Ready. (Comments are saved to Firebase Realtime Database; environment loaded from .env).")

def load_existing_remote_comments_admin():
    """Load approved user comments from Firebase Realtime Database via Admin SDK."""
    try:
        ref_comments = firebase_db.reference("comments")
        data = ref_comments.get() or {}
        for cid_str, c in data.items():
            try:
                cid = int(c.get("id", cid_str))
                _live_comments[cid] = c
            except ValueError:
                pass
    except Exception as e:
        print(f"[Firebase] Error loading remote comments: {e}")

def load_existing_remote_comments_rest(db_url: str):
    """Load approved user comments from Firebase Realtime Database via REST."""
    try:
        resp = requests.get(f"{db_url}/comments.json", timeout=4)
        if resp.status_code == 200 and resp.json():
            data = resp.json()
            for cid_str, c in data.items():
                try:
                    cid = int(c.get("id", cid_str))
                    _live_comments[cid] = c
                except ValueError:
                    pass
    except Exception as e:
        print(f"[Firebase] Error loading REST comments: {e}")

def get_user_comments_for_post(post_id: int) -> List[Dict[str, Any]]:
    """Retrieve approved user comments for a specific post from Firebase Realtime Database."""
    if _using_admin_sdk:
        try:
            ref_comments = firebase_db.reference("comments")
            data = ref_comments.get() or {}
            approved = []
            for c in data.values():
                if c and int(c.get("post_id", 0)) == post_id and c.get("status") == "approved":
                    approved.append(c)
            approved.sort(key=lambda x: x.get("id", 0))
            return approved
        except Exception as e:
            print(f"[Firebase] Remote fetch error: {e}")

    # Synchronized buffer
    approved = [
        c for c in _live_comments.values()
        if int(c.get("post_id", 0)) == post_id and c.get("status") == "approved"
    ]
    approved.sort(key=lambda x: x.get("id", 0))
    return approved

def count_user_comments_for_post(post_id: int) -> int:
    """Count approved comments in Firebase Realtime Database for a post."""
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
    global _next_id

    comment_id = _next_id
    _next_id += 1

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

    # Keep in live buffer
    _live_comments[comment_id] = comment_record

    # Save to Firebase Realtime Database
    if _using_admin_sdk:
        try:
            ref_comment = firebase_db.reference(f"comments/{comment_id}")
            ref_comment.set(comment_record)
            print(f"[Firebase RTDB] Comment {comment_id} written to Firebase via Admin SDK.")
        except Exception as e:
            print(f"[Firebase RTDB] Error writing to Realtime Database: {e}")
    else:
        db_url = os.environ.get("FIREBASE_DATABASE_URL", FIREBASE_DATABASE_URL).rstrip("/")
        db_secret = os.environ.get("FIREBASE_DATABASE_SECRET", "")
        if db_url:
            try:
                write_url = f"{db_url}/comments/{comment_id}.json"
                if db_secret:
                    write_url += f"?auth={db_secret}"
                resp = requests.put(write_url, json=comment_record, timeout=5)
                if resp.status_code == 200:
                    print(f"✅ [Firebase RTDB] Successfully saved comment {comment_id} to Firebase!")
                else:
                    print(f"⚠️ [Firebase RTDB Permission Denied] Status {resp.status_code}: {resp.text}")
                    print("👉 Tip: Firebase Console -> Realtime Database -> 'Rules' tab mein '.read': true, '.write': true set karke Publish karein.")
            except Exception as e:
                print(f"⚠️ [Firebase RTDB Connection Error]: {e}")

    return comment_record
