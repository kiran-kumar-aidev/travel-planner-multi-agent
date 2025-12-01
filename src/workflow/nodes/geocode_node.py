
from src.tools.geocode import nominatim_geocode

def geocode_node(state):
    """
    Node 1: Convert destination text → lat/lon using Nominatim.
    Works with LangGraph Pydantic state (TravelState).
    """

    # Access like Pydantic model, not dict
    destination = state.destination

    if not destination:
        raise ValueError("destination missing in state")

    geo = nominatim_geocode(destination)
    if not geo:
        raise ValueError(f"Could not find geocode info for {destination}")

    return {"geocode": geo}
