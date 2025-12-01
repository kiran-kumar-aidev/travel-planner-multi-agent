import requests
from urllib.parse import urlencode

def get_weather_forecast(lat: float, lon: float):
    """
    Get the 7-day daily weather forecast using Open-Meteo (no API key required).
    Always fetch fresh data (no caching).
    """
    url = "https://api.open-meteo.com/v1/forecast?"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto"
    }

    full_url = url + urlencode(params)
    r = requests.get(full_url, timeout=10)
    r.raise_for_status()
    return r.json()
