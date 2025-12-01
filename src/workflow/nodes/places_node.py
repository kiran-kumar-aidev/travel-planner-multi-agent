from src.tools.places import get_attractions, get_beaches, get_food
from src.workflow.state import TravelState

def places_node(state: TravelState) -> TravelState:
    geo = state.geocode
    if not geo:
        raise ValueError("Missing geocode in state")

    lat = geo["lat"]
    lon = geo["lon"]

    # Fetch full results
    attractions = get_attractions(lat, lon)
    beaches = get_beaches(lat, lon)
    food = get_food(lat, lon)

    # KEEP ONLY TOP 3 EACH → to avoid token explosion
    state.places = {
        "attractions": attractions[:3],
        "beaches": beaches[:3],
        "food": food[:3],
    }
    return state
