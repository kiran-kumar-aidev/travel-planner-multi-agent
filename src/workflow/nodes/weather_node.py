
from src.tools.weather import get_weather_forecast

def weather_node(state):
    """
    Node 2: Fetch 7-day weather forecast using Open-Meteo.
    Works with LangGraph Pydantic state.
    """

    geo = state.geocode   # Access via attribute
    if not geo:
        raise ValueError("geocode missing before weather node")

    lat = geo["lat"]
    lon = geo["lon"]
    place = geo["place"]

    forecast = get_weather_forecast(lat, lon)

    return {
        "weather": {
            "place": place,
            "lat": lat,
            "lon": lon,
            "forecast": forecast.get("daily", {})
        }
    }
