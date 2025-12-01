import requests
import time
from urllib.parse import urlencode
from src.tools.geocode_cache import get_from_cache, save_to_cache

# Polite usage for Nominatim
USER_AGENT = "agentic-travel-planner/1.0 (Duggiralakirankmr@gmail.com)"

def nominatim_geocode(place: str, max_retries: int = 3, pause: float = 1.0):
    """
    Simple Nominatim geocode (OpenStreetMap). Returns top result dict or None.
    """

    # 1️⃣ Check cache first
    cached = get_from_cache(place)
    if cached:
        return cached

    url = "https://nominatim.openstreetmap.org/search?"
    params = {
        "q": place,
        "format": "json",
        "limit": 5,
        "addressdetails": 1,
    }
    headers = {"User-Agent": USER_AGENT}

    last_err = None
    for attempt in range(max_retries):
        try:
            full = url + urlencode(params)
            r = requests.get(full, headers=headers, timeout=10)
            r.raise_for_status()
            data = r.json()

            if data:
                top = data[0]

                # 2️⃣ Build result object
                result = {
                    "place": place,
                    "lat": float(top["lat"]),
                    "lon": float(top["lon"]),
                    "display_name": top.get("display_name"),
                    "raw": top
                }

                # 3️⃣ Save to cache
                save_to_cache(place, result)

                # 4️⃣ Return result
                return result

            return None

        except Exception as e:
            last_err = e
            time.sleep(pause)

    # 5️⃣ If all retries failed
    raise last_err
