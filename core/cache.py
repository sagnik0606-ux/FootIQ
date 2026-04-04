import os
import json
from datetime import datetime, timedelta
from config import CACHE_DIR, CACHE_TTL_DAYS

os.makedirs(CACHE_DIR, exist_ok=True)


def _path(key: str) -> str:
    safe = key.replace("/", "_").replace("?", "_").replace("&", "_").replace("=", "_")
    return os.path.join(CACHE_DIR, f"{safe}.json")


def get(key: str):
    """Return cached payload or None if missing / expired."""
    p = _path(key)
    if not os.path.exists(p):
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            record = json.load(f)
        ts = datetime.fromisoformat(record["ts"])
        if datetime.now() - ts > timedelta(days=CACHE_TTL_DAYS):
            return None
        return record["data"]
    except Exception:
        return None


def put(key: str, data) -> None:
    """Persist data to cache."""
    p = _path(key)
    with open(p, "w", encoding="utf-8") as f:
        json.dump({"ts": datetime.now().isoformat(), "data": data}, f)
