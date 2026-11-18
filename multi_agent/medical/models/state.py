from typing import TypedDict, Any


class AgentState(TypedDict, total=False):

    original_query: str
    patient_id: str

    sub_queries: list[dict[str, Any]]

    lab_results: list[dict[str, Any]]
    medication_results: list[dict[str, Any]]

    final_response: dict[str, Any]


    