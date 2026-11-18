from multi_agent.medical.models.state import AgentState
from multi_agent.medical.agents.coordinator_agent import coordinator_agent
def coordinator_node(state: AgentState):
    routes = coordinator_agent(state["sub_queries"])
    return routes