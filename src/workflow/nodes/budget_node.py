
from src.agents.budget_agent import budget_agent_run

def budget_node(state):
    """
    Node 5: Budget estimation using budget_agent_run.
    Works with LangGraph Pydantic TravelState.
    """

    # Access Pydantic fields directly
    destination = state.destination
    days = state.days
    persons = state.persons
    budget_inr = state.budget_inr
    budget_tier = state.budget_tier

    # transport_total_km may or may not exist yet
    transport_distance = 0
    if state.routing and "distance_m" in state.routing:
        # Example: total distance = sum of upper triangle
        dist_matrix = state.routing["distance_m"]
        total = 0
        for i in range(len(dist_matrix)):
            for j in range(i+1, len(dist_matrix[i])):
                total += dist_matrix[i][j]
        transport_distance = total / 1000.0  # convert m → km

    request = {
        "destination": destination,
        "days": days,
        "persons": persons,
        "budget_inr": budget_inr,
        "budget_tier": budget_tier,
        "transport_total_km": transport_distance,
    }

    result = budget_agent_run(request)

    return {"budget": result}
