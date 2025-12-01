
from typing import Dict, Any
from src.tools.geocode import nominatim_geocode
from src.tools.weather import get_weather_forecast


def weather_agent_run(place: str) -> Dict[str, Any]:
    """
    Weather Agent:
    1. Geocodes the place (Goa → lat/lon)
    2. Fetches 7-day weather forecast
    3. Returns clean structured summary
    """
    # Step 1 — Geocode
    geo = nominatim_geocode(place)
    if not geo:
        return {
            "place": place,
            "error": "Geocoding failed. Try a more specific location."
        }

    lat = geo["lat"]
    lon = geo["lon"]

    # Step 2 — Fetch weather
    weather = get_weather_forecast(lat, lon)
    if not weather:
        return {
            "place": place,
            "lat": lat,
            "lon": lon,
            "error": "Weather API failed."
        }

    # Step 3 — Build readable summary
    daily = weather.get("daily", {})
    
    result = {
        "place": geo["display_name"],
        "lat": lat,
        "lon": lon,
        "forecast": []
    }

    times = daily.get("time", [])
    tmax = daily.get("temperature_2m_max", [])
    tmin = daily.get("temperature_2m_min", [])
    rain = daily.get("precipitation_sum", [])

    for i in range(len(times)):
        result["forecast"].append({
            "date": times[i],
            "temp_max_c": tmax[i],
            "temp_min_c": tmin[i],
            "rain_mm": rain[i]
        })

    return result
