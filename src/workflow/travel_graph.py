
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

# Import all nodes
from src.workflow.nodes.geocode_node import geocode_node
from src.workflow.nodes.weather_node import weather_node
from src.workflow.nodes.places_node import places_node
from src.workflow.nodes.routing_node import routing_node
from src.workflow.nodes.budget_node import budget_node
from src.workflow.nodes.itinerary_node import itinerary_node


# -------------------------
# Define state structure
# -------------------------

class TravelState(BaseModel):
    # User input
    destination: Optional[str] = None
    days: int = 5
    persons: int = 1
    budget_inr: int = 30000
    budget_tier: str = "mid"

    # Outputs from nodes
    geocode: Optional[dict] = None
    weather: Optional[dict] = None
    places: Optional[dict] = None
    routing: Optional[dict] = None
    budget: Optional[dict] = None
    itinerary: Optional[dict] = None


# -------------------------
# Build the workflow graph
# -------------------------

workflow = StateGraph(TravelState)

# Register nodes
workflow.add_node("geocode", geocode_node)
workflow.add_node("weather", weather_node)
workflow.add_node("places", places_node)
workflow.add_node("routing", routing_node)
workflow.add_node("budget", budget_node)
workflow.add_node("itinerary", itinerary_node)

# Set entry point
workflow.set_entry_point("geocode")

# Add edges
workflow.add_edge("geocode", "weather")
workflow.add_edge("weather", "places")
workflow.add_edge("places", "routing")
workflow.add_edge("routing", "budget")
workflow.add_edge("budget", "itinerary")
workflow.add_edge("itinerary", END)

# Compile
app = workflow.compile()
