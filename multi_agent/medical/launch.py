from multi_agent.medical.nodes.lab_node import lab_node
from multi_agent.medical.nodes.medication_node import medication_node
import json

from langgraph.graph import StateGraph, START, END

from multi_agent.medical.models.state import AgentState
from multi_agent.medical.nodes.query_node import query_node
from multi_agent.medical.nodes.coordinator_node import coordinator_node
from multi_agent.medical.nodes.response_node import response_node


def run():

    builder = StateGraph(AgentState)

    builder.add_node("query", query_node)
    builder.add_node("lab", lab_node)
    builder.add_node("medication", medication_node)
    builder.add_node("response", response_node)

    builder.add_edge(START, "query")

    builder.add_conditional_edges(
        "query",
        coordinator_node,
        {
            "lab": "lab",
            "medication": "medication",
            "response": "response"
        }
    )

    builder.add_edge("lab", "response")
    builder.add_edge("medication", "response")
    builder.add_edge("response", END)

    graph = builder.compile()
    query  = (
            "Find the latest HbA1c result and "
            "diabetes medication for patient P001"
        )
    print(f"QUERY {query}")   

    result = graph.invoke({
        "original_query": query
    })

    print("\n========== FINAL RESPONSE ==========")

    print(json.dumps(
        result["final_response"],
        indent=4
    ))
