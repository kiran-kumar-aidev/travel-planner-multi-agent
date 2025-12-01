"""
Pairwise driving-time/distance matrix helper using OSRM.

Functions:
- compute_matrix_from_places(places, pause_s=0.2) -> dict
- pretty_print_matrix(matrix_dict) -> None

`places` should be an iterable of dicts with keys:
  - "name" (str)
  - "lat"  (float)
  - "lon"  (float)

Example place item:
  {"name": "Fort Aguada", "lat": 15.470, "lon": 73.765}

This module calls src.tools.routing.osrm_route(...) for pairwise routing.
"""
import time
from typing import List, Dict, Any
from src.tools.routing import osrm_route

def _ensure_place_fields(place: Dict[str,Any]):
    if not all(k in place for k in ("name","lat","lon")):
        raise ValueError("Each place must have 'name','lat','lon' keys")

def compute_matrix_from_places(places: List[Dict[str,Any]], pause_s: float = 0.2) -> Dict[str, Any]:
    """
    Compute pairwise driving matrix for given places.
    - places: list of {"name", "lat", "lon"}
    - pause_s: pause between OSRM requests (politeness)
    Returns a dict:
    {
      "names": [name1,...],
      "distance_m": [[0, d12, ...], [...], ...],
      "duration_s": [[0, t12, ...], [...], ...],
      "distance_readable": [[...], ...],
      "duration_readable": [[...], ...]
    }
    """
    n = len(places)
    if n == 0:
        return {}

    # Validate
    for p in places:
        _ensure_place_fields(p)

    names = [p["name"] for p in places]
    # initialize matrices
    distance_m = [[0.0]*n for _ in range(n)]
    duration_s = [[0.0]*n for _ in range(n)]
    distance_str = [["-"]*n for _ in range(n)]
    duration_str = [["-"]*n for _ in range(n)]

    # compute pairwise (i -> j) for i != j
    for i in range(n):
        for j in range(n):
            if i == j:
                distance_m[i][j] = 0.0
                duration_s[i][j] = 0.0
                distance_str[i][j] = "0 m"
                duration_str[i][j] = "0s"
                continue

            a = places[i]
            b = places[j]

            # polite pause
            time.sleep(pause_s)

            try:
                res = osrm_route(a["lat"], a["lon"], b["lat"], b["lon"], mode="driving")
            except Exception as e:
                # If OSRM fails for this pair, store large sentinel and continue
                # This allows planning to continue rather than crash.
                print(f"[warning] OSRM route failed for {a['name']} -> {b['name']}: {e}")
                distance_m[i][j] = float("inf")
                duration_s[i][j] = float("inf")
                distance_str[i][j] = "∞"
                duration_str[i][j] = "∞"
                continue

            distance_m[i][j] = res.get("distance_m", 0.0)
            duration_s[i][j] = res.get("duration_s", 0.0)
            distance_str[i][j] = res.get("distance", "")
            duration_str[i][j] = res.get("duration", "")

    return {
        "names": names,
        "distance_m": distance_m,
        "duration_s": duration_s,
        "distance_readable": distance_str,
        "duration_readable": duration_str,
    }


def pretty_print_matrix(matrix: Dict[str,Any]) -> None:
    """Prints a readable matrix to console (names + durations)."""
    names = matrix["names"]
    dur = matrix["duration_readable"]
    n = len(names)

    # header
    header = ["From \\ To"] + names
    row_fmt = "{:20}" + ("{:>12}" * n)
    print(row_fmt.format(*header))
    for i in range(n):
        row = [names[i]] + [dur[i][j] for j in range(n)]
        print(row_fmt.format(*row))
