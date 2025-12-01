"""
Simple OSRM routing helper for the Agentic Travel Planner POC.

Functions:
- osrm_route(lat_from, lon_from, lat_to, lon_to, mode='driving') -> dict
- format_duration(seconds) -> str
- format_distance(meters) -> str

"""

import requests
from typing import Dict

OSRM_BASE = "https://router.project-osrm.org/route/v1"

def _validate_mode(mode: str) -> str:
    mode = mode.lower()
    if mode not in ("driving", "walking", "cycling"):
        raise ValueError("mode must be one of 'driving', 'walking', 'cycling'")
    return mode

def osrm_route(lat_from: float, lon_from: float, lat_to: float, lon_to: float, mode: str = "driving") -> Dict:
    """
    Query OSRM route service and return summary.

    Returns dict:
    {
      "distance_m": 1234.5,
      "duration_s": 567.8,
      "distance": "1.23 km",
      "duration": "9m 27s",
      "raw": <original json>
    }
    """
    mode = _validate_mode(mode)
    # OSRM expects lon,lat pairs
    coord_str = f"{lon_from},{lat_from};{lon_to},{lat_to}"

    url = f"{OSRM_BASE}/{mode}/{coord_str}"
    params = {
        "overview": "false",      
        "alternatives": "false",
        "steps": "false"
    }

    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    payload = resp.json()

    # Basic validation
    if "routes" not in payload or not payload["routes"]:
        raise RuntimeError("OSRM returned no routes for the given coordinates")

    route = payload["routes"][0]
    distance_m = float(route.get("distance", 0.0))
    duration_s = float(route.get("duration", 0.0))

    return {
        "distance_m": distance_m,
        "duration_s": duration_s,
        "distance": format_distance(distance_m),
        "duration": format_duration(duration_s),
        "raw": payload
    }

def format_duration(seconds: float) -> str:
    """Return human readable duration, e.g. '1h 12m' or '9m 30s'."""
    s = int(round(seconds))
    if s < 60:
        return f"{s}s"
    mins = s // 60
    if mins < 60:
        return f"{mins}m {s % 60}s"
    hours = mins // 60
    mins = mins % 60
    return f"{hours}h {mins}m"

def format_distance(meters: float) -> str:
    """Return human readable distance, e.g. '1.2 km' or '750 m'."""
    m = float(meters)
    if m >= 1000:
        return f"{m/1000:.2f} km"
    return f"{int(round(m))} m"
