from multi_agent.medical.agents.query_agent import query_decomposer
from multi_agent.medical.models.state import AgentState


def query_node(state: AgentState):

    result = query_decomposer(state["original_query"])

    return {
        "patient_id": result["patient_id"],
        "sub_queries": result["sub_queries"]
    }
