# src/data/pricing_model.py
"""
Simple pricing model (simulated) for POC.

All currency values are INR (₹).
These are conservative estimations / ranges you can refine later.
"""

from typing import Tuple, Dict, Any
import random

# Flight price rough ranges by region (per person, round-trip, INR)
FLIGHT_RANGES = {
    "vietnam": (18000, 32000),
    "thailand": (12000, 22000),
    "malaysia": (15000, 26000),
    "sri_lanka": (9000, 16000),
    "bali": (16000, 28000),
    "dubai": (18000, 35000),
    "domestic": (3000, 9000),
}

# Hotel price per night by tier (INR/night)
HOTEL_TIER = {
    "budget": (800, 1500),     # cheap hotels / guesthouses
    "mid": (1800, 3500),       # 3-star to nice guesthouse
    "premium": (4000, 9000),   # 4-5 star range
}

# Meal per day per person (INR)
MEAL_COST_PER_DAY = {
    "budget": 400,
    "mid": 900,
    "premium": 1800,
}

# Local transport cost per km (INR/km) - rough
TRANSPORT_PER_KM = {
    "india": 15,
    "vietnam": 20,
    "thailand": 22,
    "malaysia": 28,
    "sri_lanka": 18,
    "bali": 30,
    "dubai": 35,
    "default": 25
}

# Sightseeing / attraction average per day (INR) — tickets, minor expenses
SIGHTSEEING_PER_DAY = {
    "budget": 300,
    "mid": 800,
    "premium": 1500
}

# Utility helpers
def sample_range(rng: Tuple[int,int]) -> int:
    """Return a reasonable representative value from a range (median-ish)."""
    lo, hi = rng
    # Use weighted average slightly skewed to lower half to be conservative
    return int(lo + (hi - lo) * 0.45)


def estimate_flight_cost(destination: str, origin: str = "india", persons: int = 1) -> int:
    key = destination.strip().lower()
    rng = FLIGHT_RANGES.get(key, FLIGHT_RANGES.get("domestic"))
    return sample_range(rng) * persons


def estimate_hotel_cost(nights: int, tier: str = "mid", persons: int = 1) -> int:
    """Estimate hotel total cost for persons. Hotel tiers are priced per room/night; assume 1 room per 2 persons."""
    tier = tier if tier in HOTEL_TIER else "mid"
    per_night = sample_range(HOTEL_TIER[tier])
    rooms = max(1, persons // 2 + (1 if persons % 2 else 0))
    return per_night * nights * rooms


def estimate_meals_cost(days: int, tier: str = "mid", persons: int = 1) -> int:
    per_person = MEAL_COST_PER_DAY.get(tier, MEAL_COST_PER_DAY["mid"])
    return per_person * days * persons


def estimate_local_transport_cost(total_km: float, country: str = "default") -> int:
    per_km = TRANSPORT_PER_KM.get(country.lower(), TRANSPORT_PER_KM["default"])
    return int(total_km * per_km)


def estimate_sightseeing_cost(days: int, tier: str = "mid", persons: int = 1) -> int:
    per_person_day = SIGHTSEEING_PER_DAY.get(tier, SIGHTSEEING_PER_DAY["mid"])
    return per_person_day * days * persons


def default_daily_local_km(days: int, mode: str = "city") -> float:
    """
    Provide a simple estimation of daily travel distance (km).
    - city mode: tourist city days -> 20-50 km/day
    - multi-city: transit days -> higher
    """
    if mode == "city":
        return 30.0 * days
    if mode == "multi_city":
        return 80.0 * days
    return 30.0 * days
