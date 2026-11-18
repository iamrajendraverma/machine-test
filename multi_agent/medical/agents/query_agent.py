import re

# Lab tests the agent knows, keyed by the word that appears in the query.
# Values match the test_name used in multi_agent/medical/data.py.
LAB_TESTS = {
    "hba1c": "HbA1c",
    "urine": "Urine Test",
    "cbc": "Complete Blood Count",
    "blood test": "Blood Test"
}

def query_decomposer(query):
    # Step 1: Extract patient ID
    match = re.search(r'\bP\d+\b', query)

    if not match:
        raise ValueError("Patient ID not found")

    patient_id = match.group()

    # Step 2: Identify query categories
    sub_queries = []
    query_lower = query.lower()

    # Step 3: Lab intent
    """
    word in query_lower 
    hba1c in query_loer -> true
    hba1c in query_loer -> false
    hba1c in query_loer -> false  
    """
    if any(word in query_lower for word in
           ["hba1c", "lab", "blood test"]):

        # None means a generic lab request with no specific test named.
        test_name = next(
            (name for key, name in LAB_TESTS.items() if key in query_lower),
            None,
        )

        sub_queries.append({
            "test_name": test_name,
            "category": "lab",
            "query": "Find the latest HbA1c result"
        })
    # Step 4: Medication intent
    if any(word in query_lower for word in
           ["medication", "medicine", "drug"]):

        sub_queries.append({
            "category": "medication",
            "query": "Find patient medication records"
        })
    return {
        "patient_id": patient_id,
        "sub_queries": sub_queries
    }
