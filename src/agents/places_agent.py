from typing import Dict
from src.tools.geocode import nominatim_geocode
from src.tools.places import (
    get_attractions,
    get_beaches,
    get_food
)


def places_agent_run(place: str, radius: int = 15000, limit: int = 10) -> Dict:
    """
    Places Agent:
    1. Geocodes the location
    2. Fetches attractions / beaches / food places
    3. Returns clean structured data
    """

    geo = nominatim_geocode(place)
    if not geo:
        return {"error": "Geocoding failed", "place": place}

    lat = geo["lat"]
    lon = geo["lon"]

    # Fetch raw data
    attractions = get_attractions(lat, lon, radius=radius, limit=limit)
    beaches = get_beaches(lat, lon, radius=radius, limit=limit)
    food_places = get_food(lat, lon, radius=radius, limit=limit)

    # Normalize Geoapify response
    def normalize(data):
        if isinstance(data, dict) and "features" in data:
            return data["features"]
        if isinstance(data, list):
            return data
        return []

    return {
        "place": geo["display_name"],
        "lat": lat,
        "lon": lon,
        "attractions": normalize(attractions),
        "beaches": normalize(beaches),
        "food": normalize(food_places),
    }
