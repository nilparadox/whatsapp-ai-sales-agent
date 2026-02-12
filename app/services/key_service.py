import json
from pathlib import Path
from typing import Dict

KEYS_PATH = Path("data/business_keys.json")

def load_keys() -> Dict[str, str]:
    if not KEYS_PATH.exists():
        return {}
    return json.loads(KEYS_PATH.read_text(encoding="utf-8") or "{}")

def get_key(business_id: str) -> str:
    keys = load_keys()
    return keys.get(business_id, "")
