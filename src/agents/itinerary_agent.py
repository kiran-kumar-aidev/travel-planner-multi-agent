import os
from groq import Groq

def itinerary_agent_run(data: dict):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    budget = data["budget"]
    weather = data["weather"]
    places = data["places"]
    routing = data["routing_summary"]

    # -----------------------------
    # FIXED WEATHER COMPRESSION
    # -----------------------------
    forecast = weather.get("forecast", {})

    compressed_weather = []
    if isinstance(forecast, dict):
        dates = forecast.get("time", [])
        tmax = forecast.get("temperature_2m_max", [])
        tmin = forecast.get("temperature_2m_min", [])
        rain = forecast.get("precipitation_sum", [])

        for i in range(min(2, len(dates))):
            compressed_weather.append({
                "date": dates[i],
                "max": tmax[i],
                "min": tmin[i],
                "rain": rain[i]
            })

    # -----------------------------
    # PLACES COMPRESSED
    # -----------------------------
    top_attractions = [p["name"] for p in places.get("attractions", [])]
    top_beaches = [p["name"] for p in places.get("beaches", [])]
    top_food = [p["name"] for p in places.get("food", [])]

    # -----------------------------
    # PROMPT
    # -----------------------------
    prompt = f"""
You are an expert travel planner.

Destination: {budget['breakdown']['destination']}
Days: {budget['breakdown']['days']}
Budget: ₹{budget['breakdown']['total_estimated']}

Weather (next 2 days):
{compressed_weather}

Top Attractions: {top_attractions}
Top Beaches: {top_beaches}
Food Places: {top_food}

Travel Time (summary):
{routing.get('summary')}

Write a clear, friendly, day-by-day itinerary:
- Morning / Afternoon / Evening plan
- Places to visit
- Food suggestions
- Short budget usage summary
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.6,
    )

    return response.choices[0].message.content

