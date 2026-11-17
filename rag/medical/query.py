"""Turn a free-text medical question into structured sub-queries."""

import re

PATIENT_PATTERN = re.compile(r"patient\s+(P\d+)", re.IGNORECASE)

QUERY_TYPES = {
    "hba1c": {
        "keywords": ["hba1c", "blood sugar"],
        "document_types": ["lab_report"],
        "instruction": "Find HbA1c results and identify the latest record.",
    },
    "medications": {
        "keywords": ["medication", "medications", "medicine",
                     "medicines", "prescribed"],
        "document_types": ["prescription"],
        "instruction": "Find prescribed medications.",
    },
    "allergies": {
        "keywords": ["allergy", "allergies", "allergic"],
        "document_types": ["consultation"],
        "instruction": "Find reported allergies.",
    },
    "imaging": {
        "keywords": ["x-ray", "xray", "imaging", "scan"],
        "document_types": ["imaging"],
        "instruction": "Find relevant imaging reports.",
    },
}


def extract_patient_id(query):
    match = PATIENT_PATTERN.search(query)
    return match.group(1).upper() if match else None


def decompose_query(query):
    query_lower = query.lower()
    patient_id = extract_patient_id(query)

    sub_queries = [
        {
            "category": category,
            "query": details["instruction"],
            "patient_id": patient_id,
            "document_types": details["document_types"],
        }
        for category, details in QUERY_TYPES.items()
        if any(keyword in query_lower for keyword in details["keywords"])
    ]

    return {
        "original_query": query,
        "patient_id": patient_id,
        "sub_queries": sub_queries,
    }
