from src.tools.routing_matrix import compute_matrix_from_places

def routing_node(state):
    """
    Node 4: Build routing matrix from selected top places.
    """
    # Pydantic models don't have get(), so use attribute access
    places_data = state.places

    if not places_data:
        raise ValueError("places missing in state")

    attractions = places_data.get("attractions", [])
    beaches = places_data.get("beaches", [])
    food = places_data.get("food", [])

    # Pick top 3 attractions + top 1 beach + top 1 food
    selected = []

    def convert_feature(f):
        props = f.get("properties", {})
        name = (
            props.get("name")
            or props.get("address_line1")
            or "POI"
        )
        return {
            "name": name,
            "lat": props.get("lat"),
            "lon": props.get("lon"),
        }

    for f in attractions[:3]:
        selected.append(convert_feature(f))

    if beaches:
        selected.append(convert_feature(beaches[0]))

    if food:
        selected.append(convert_feature(food[0]))

    # Remove invalid entries
    selected = [p for p in selected if p["lat"] and p["lon"]]

    if not selected:
        # still keep routing key so next node doesn't break
        state.routing = {
            "names": [],
            "duration_readable": [[]],
        }
        return state

    # Compute routing matrix
    matrix = compute_matrix_from_places(selected)
    state.routing = matrix
    return state
