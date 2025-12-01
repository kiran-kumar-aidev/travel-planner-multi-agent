import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

API_KEY = os.getenv("GEOAPIFY_API_KEY")
BASE_URL = "https://api.geoapify.com/v2/places"

if not API_KEY:
    raise ValueError("GEOAPIFY_API_KEY missing in .env")


def _fetch_places(lat: float, lon: float, category: str, radius: int = 5000, limit: int = 20) -> Dict[str, Any]:
    """
    Low-level Geoapify request.
    """
    params = {
        "categories": category,
        "filter": f"circle:{lon},{lat},{radius}",
        "limit": limit,
        "apiKey": API_KEY
    }
    url = BASE_URL + "?" + urlencode(params)

    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.json()


def _simplify_feature(feat: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert raw Geoapify feature into a small, clean dict.
    """
    p = feat.get("properties", {})
    geom = feat.get("geometry", {})
    coords = geom.get("coordinates", [None, None])

    return {
        "name": p.get("name") or p.get("formatted"),
        "lat": p.get("lat") or coords[1],
        "lon": p.get("lon") or coords[0],
        "formatted": p.get("formatted"),
        "categories": p.get("categories", []),
        "place_id": p.get("place_id"),
    }


# ------------------ FINAL PUBLIC FUNCTIONS ---------------------- #

def get_attractions(lat: float, lon: float, radius=10000, limit=20):
    """Tourist attractions only."""
    raw = _fetch_places(lat, lon, "tourism.attraction", radius, limit)
    return [_simplify_feature(f) for f in raw.get("features", [])]


def get_beaches(lat: float, lon: float, radius=30000, limit=20):
    """
    Beaches & coastline:
    - natural.water.sea
    - natural.water.ocean
    We also fallback to general 'natural' if nothing found.
    """
    try:
        raw = _fetch_places(
            lat, lon,
            "natural.water.sea,natural.water.ocean",
            radius, limit
        )
        feats = raw.get("features", [])
        if feats:
            return [_simplify_feature(f) for f in feats]
    except:
        pass  # fallback below

    # fallback (general nature)
    raw = _fetch_places(lat, lon, "natural", radius, limit)
    return [_simplify_feature(f) for f in raw.get("features", [])]


def get_nature(lat: float, lon: float, radius=15000, limit=20):
    """Natural features — waterfalls, hills, lakes, etc."""
    raw = _fetch_places(lat, lon, "natural", radius, limit)
    return [_simplify_feature(f) for f in raw.get("features", [])]


def get_food(lat: float, lon: float, radius=8000, limit=20):
    """
    Restaurants & food places:
    - catering.restaurant
    - catering.fast_food
    - catering.cafe
    """
    raw = _fetch_places(
        lat, lon,
        "catering.restaurant,catering.fast_food,catering.cafe",
        radius, limit
    )
    return [_simplify_feature(f) for f in raw.get("features", [])]


def get_entertainment(lat: float, lon: float, radius=12000, limit=20):
    """Entertainment spots."""
    raw = _fetch_places(lat, lon, "entertainment,leisure", radius, limit)
    return [_simplify_feature(f) for f in raw.get("features", [])]


def get_place_by_id(place_id: str):
    raise NotImplementedError(
        "Geoapify free tier DOES NOT support place-detail lookup. Use maps or Overpass API instead."
    )
