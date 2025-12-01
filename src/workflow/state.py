from typing import Optional, Dict, Any
from pydantic import BaseModel

class TravelState(BaseModel):
    destination: Optional[str] = None
    days: Optional[int] = 7
    persons: Optional[int] = 1
    budget_inr: Optional[int] = 30000
    budget_tier: Optional[str] = "mid"

    geocode: Optional[Dict[str, Any]] = None
    weather: Optional[Dict[str, Any]] = None
    places: Optional[Dict[str, Any]] = None
    routing: Optional[Dict[str, Any]] = None
    budget: Optional[Dict[str, Any]] = None
    itinerary: Optional[Dict[str, Any]] = None
