from multi_agent.medical.models.state import AgentState
from multi_agent.medical.agents.medication_agent import medication_agent


def medication_node(state: AgentState):

    patient_id = state["patient_id"]

    # Select medication subqueries
    medication_queries = [
        item for item in state["sub_queries"]
        if item["category"] == "medication"
    ]

    if not medication_queries:
        return {
            "medication_results": []
        }

    results = medication_agent(patient_id)

    return {
        "medication_results": results
    }