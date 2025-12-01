from src.workflow.state import TravelState
from src.agents.itinerary_agent import itinerary_agent_run

def itinerary_node(state: TravelState) -> TravelState:
    if not state.budget:
        raise ValueError("Missing budget info in state")
    if not state.weather:
        raise ValueError("Missing weather info in state")
    if not state.places:
        raise ValueError("Missing places info in state")
    if not state.routing:
        raise ValueError("Missing routing matrix in state")

    # COMPRESS routing matrix
    routing_small = {
        "summary": state.routing.get("duration_readable", [])[:3]
    }

    # Call LLM agent with compressed info
    itinerary_text = itinerary_agent_run(
        {
            "budget": state.budget,
            "weather": state.weather,
            "places": state.places,
            "routing_summary": routing_small,
        }
    )

    state.itinerary = itinerary_text
    return state
