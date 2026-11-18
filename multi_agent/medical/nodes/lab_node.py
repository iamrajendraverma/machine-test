from multi_agent.medical.models.state import AgentState
from multi_agent.medical.agents.lab_agent import lab_agent

def lab_node(state: AgentState):

    patient_id = state["patient_id"]

    # Get only lab subqueries
    lab_queries = [
        item for item in state["sub_queries"]
        if item["category"] == "lab"
    ]

    all_results = []

    for sub_query in lab_queries:

        test_name = sub_query["test_name"]

        results = lab_agent(patient_id, test_name)

        all_results.extend(results)

    return {
        "lab_results": all_results
    }