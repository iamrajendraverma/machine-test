from multi_agent.medical.models.state import AgentState
from multi_agent.medical.agents.response_agent import response_agent


def response_node(state: AgentState):

    lab_results = state.get("lab_results", [])
    medication_results = state.get("medication_results", [])

    result = response_agent(
        lab_results,
        medication_results
    )

    return {
        "final_response": result
    }