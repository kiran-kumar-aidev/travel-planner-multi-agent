from typing import Dict, List
from src.tools.routing_matrix import compute_matrix_from_places


def routing_agent_run(places: List[Dict]) -> Dict:
    """
    Routing Agent:
    Input: list of places with lat/lon
    Output:
        - durations
        - distances
        - readable formats
    """

    if not places or len(places) < 2:
        return {"error": "Need at least 2 places for routing."}

    matrix = compute_matrix_from_places(places)

    return {
        "places": places,
        "names": matrix.get("names"),
        "distance_m": matrix.get("distance_m"),
        "duration_s": matrix.get("duration_s"),
        "distance_readable": matrix.get("distance_readable"),
        "duration_readable": matrix.get("duration_readable"),
    }
