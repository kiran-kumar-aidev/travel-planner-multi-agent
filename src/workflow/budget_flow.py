
from typing import TypedDict, Optional, Dict, Any
from langgraph.graph import StateGraph, END
from src.agents.budget_agent import budget_agent_run


class BudgetState(TypedDict, total=False):
    """
    State passed through the LangGraph for budget evaluation.

    Fields:
      destination: e.g., "vietnam"
      days: int
      budget_inr: int
      persons: int
      budget_tier: "budget" | "mid" | "premium"
      transport_total_km: float (optional)
      budget_result: dict (output from budget_agent_run)
    """
    destination: str
    days: int
    budget_inr: int
    persons: int
    budget_tier: str
    transport_total_km: float
    budget_result: Dict[str, Any]


def budget_node(state: BudgetState) -> BudgetState:
    """
    Single node that calls the Budget Agent with current state info.
    """
    req = {
        "destination": state.get("destination"),
        "days": state.get("days", 3),
        "budget_inr": state.get("budget_inr", 0),
        "persons": state.get("persons", 1),
        "budget_tier": state.get("budget_tier", "mid"),
        "transport_total_km": state.get("transport_total_km", None),
    }
    result = budget_agent_run(req)
    # write result into state
    state["budget_result"] = result
    return state


def build_budget_graph():
    """
    Build a simple LangGraph with a single budget node.
    """
    graph = StateGraph(BudgetState)

    # add node
    graph.add_node("budget_agent", budget_node)

    # entry point: start at budget_agent
    graph.set_entry_point("budget_agent")

    # after budget_agent, we are done
    graph.add_edge("budget_agent", END)

    return graph.compile()


def run_example():
    """
    Small helper to run a Vietnam 7-day example through the graph.
    """
    app = build_budget_graph()

    initial_state: BudgetState = {
        "destination": "vietnam",
        "days": 7,
        "budget_inr": 50000,
        "persons": 1,
        "budget_tier": "mid",
        "transport_total_km": 200.0,
    }

    # app.invoke returns the final state after graph execution
    final_state = app.invoke(initial_state)
    return final_state


if __name__ == "__main__":
    result = run_example()
    import pprint
    pprint.pprint(result)
