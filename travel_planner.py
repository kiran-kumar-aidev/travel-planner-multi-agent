from src.workflow.travel_graph import app, TravelState
import sys
from pprint import pprint

if __name__ == "__main__":
    # Take destination from argument
    if len(sys.argv) < 2:
        print("Usage: python travel_planner.py \"Goa, India\"")
        sys.exit(1)

    destination = sys.argv[1]

    # Initial state
    state = TravelState(
        destination=destination,
        days=5,
        persons=1,
        budget_inr=30000,
        budget_tier="mid"
    )

    # Run the graph
    result = app.invoke(state)

    # Print the final itinerary
    pprint(result["itinerary"])

