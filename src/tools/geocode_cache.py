import json
from pathlib import Path

CACHE_FILE = Path("geocode_cache.json")

def load_cache():
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except Exception:
            return {}
    return {}

def save_cache(cache: dict):
    CACHE_FILE.write_text(json.dumps(cache, indent=2))

def get_from_cache(place: str):
    cache = load_cache()
    return cache.get(place.lower())

def save_to_cache(place: str, data: dict):
    cache = load_cache()
    cache[place.lower()] = data
    save_cache(cache)
