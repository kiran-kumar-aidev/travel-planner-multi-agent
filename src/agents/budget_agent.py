"""
Budget Agent — evaluates whether a trip fits a user's budget and provides breakdowns
and suggestions. Uses pricing_model for simulated estimates.
"""

from typing import Dict, Any, List, Optional
from src.data.pricing_model import (
    estimate_flight_cost,
    estimate_hotel_cost,
    estimate_meals_cost,
    estimate_local_transport_cost,
    estimate_sightseeing_cost,
    default_daily_local_km
)

def estimate_trip_cost(
    destination: str,
    days: int,
    budget_tier: str = "mid",       # "budget" | "mid" | "premium"
    persons: int = 1,
    origin: str = "india",
    hotel_tier: Optional[str] = None,
    transport_total_km: Optional[float] = None
) -> Dict[str, Any]:
    """
    Return a cost breakdown for the requested trip.
    - destination: e.g., "vietnam"
    - days: integer days
    - budget_tier: "budget", "mid", "premium"
    - persons: number of travellers
    - transport_total_km: optional estimate of total local travel km (if available, e.g. from routing matrix)
    """
    # choose hotel tier if not provided (map budget_tier -> hotel tier)
    tier_map = {"budget": "budget", "mid": "mid", "premium": "premium"}
    hotel_tier = hotel_tier or tier_map.get(budget_tier, "mid")

    # Flight estimate
    flight = estimate_flight_cost(destination, origin, persons)

    # Hotel nights = days (simpler) or days-1 as you prefer
    nights = max(1, days)
    hotel = estimate_hotel_cost(nights, hotel_tier, persons)

    # Meals
    meals = estimate_meals_cost(days, budget_tier, persons)

    # Sightseeing
    sightseeing = estimate_sightseeing_cost(days, budget_tier, persons)

    # Local transport: if caller provided per-trip total_km, use that, otherwise use default heuristic
    if transport_total_km is None:
        transport_total_km = default_daily_local_km(days, mode="city")
    local_transport = estimate_local_transport_cost(transport_total_km, destination)

    # Misc (buffer) e.g., visa, tips, contingency = 8% of subtotal
    subtotal = flight + hotel + meals + sightseeing + local_transport
    contingency = int(subtotal * 0.08)

    total = subtotal + contingency

    breakdown = {
        "destination": destination,
        "days": days,
        "persons": persons,
        "flight": int(flight),
        "hotel": int(hotel),
        "meals": int(meals),
        "sightseeing": int(sightseeing),
        "local_transport": int(local_transport),
        "contingency": int(contingency),
        "total_estimated": int(total),
        "notes": "Simulated estimates; refine pricing_model for production"
    }

    return breakdown


def assess_budget_fit(budget_inr: int, breakdown: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare user budget to the estimated total and give advice/suggestions.
    """
    total = breakdown["total_estimated"]
    diff = budget_inr - total
    fit = diff >= 0

    advice = []
    if fit:
        advice.append("Your budget covers the estimated trip cost.")
    else:
        advice.append("Your budget is insufficient for the current estimated itinerary.")
        # Suggest options to reduce cost
        advice.append("Options to fit budget:")
        advice.append("- Reduce trip length by 1-2 days")
        advice.append("- Choose cheaper hotel tier (budget)")
        advice.append("- Consider a closer or cheaper destination (e.g., Sri Lanka or domestic)")
        advice.append("- Travel off-season for lower flights/hotels")

    return {
        "budget_provided": budget_inr,
        "estimated_total": total,
        "difference": int(diff),
        "fits": bool(fit),
        "advice": advice
    }


def suggest_alternatives(budget_inr: int, days: int, persons: int = 1) -> List[Dict[str, Any]]:
    """
    Return a (short) list of cheaper destinations with estimated totals
    to help user choose alternatives. helper text
    """
    candidates = ["sri_lanka", "thailand", "malaysia", "domestic"]
    suggestions = []
    for dest in candidates:
        breakdown = estimate_trip_cost(dest, days, budget_tier="mid", persons=persons)
        suggestions.append({"destination": dest, "estimated_total": breakdown["total_estimated"]})
    # Only return those under budget (sorted ascending)
    under = sorted([s for s in suggestions if s["estimated_total"] <= budget_inr], key=lambda x: x["estimated_total"])
    return under or suggestions[:3]


def budget_agent_run(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point for the Budget Agent.
    Request example:
    {
      "destination": "vietnam",
      "days": 7,
      "budget_inr": 50000,
      "persons": 1,
      "budget_tier": "mid",
      "transport_total_km": 200.0
    }
    """
    dest = request.get("destination")
    days = int(request.get("days", 3))
    budget_inr = int(request.get("budget_inr", 0))
    persons = int(request.get("persons", 1))
    tier = request.get("budget_tier", "mid")
    transport_km = request.get("transport_total_km", None)

    breakdown = estimate_trip_cost(dest, days, budget_tier=tier, persons=persons, transport_total_km=transport_km)
    assessment = assess_budget_fit(budget_inr, breakdown)
    alternatives = []
    if not assessment["fits"]:
        alternatives = suggest_alternatives(budget_inr, days, persons)

    return {
        "breakdown": breakdown,
        "assessment": assessment,
        "alternatives": alternatives
    }
