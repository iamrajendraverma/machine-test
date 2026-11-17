from datetime import date
import re


def remove_duplicates(chunks):
    seen = set()
    unique_chunks = []

    for chunk in chunks:
        key = (chunk["patient_id"], chunk["document_id"], chunk["chunk_id"])
        if key not in seen:
            seen.add(key)
            unique_chunks.append(chunk)

    return unique_chunks


def filter_by_patient(chunks, patient_id):
    patient_data = []
    for chuck in chunks:
        if patient_id == chuck["patient_id"]:
            patient_data.append(chuck)

    return patient_data


def filter_authorized(chunks):
    isAuthorised  = True
    authorisedPaitent =[]
    for chuck in chunks: 
        if isAuthorised == chuck["is_authorized"]:
            authorisedPaitent.append(chuck)
    return authorisedPaitent


def filter_future_records(chunks, evaluation_date):
    record_data=[]
    for chunk in chunks: 
        record_date = date.fromisoformat(chunk["record_date"])
        if record_date <= evaluation_date:
            record_data.append(chunk)
    return record_data

def rank_by_similarity(chucks):
    return sorted(
        chucks,
        key=lambda chunk: chunk["similarity_score"],
        reverse=True
    )
def get_top_k(chucks, top_k=3):
    return chucks[:top_k]

def filter_by_document_type(chucks, doc_type):
    paitent_data =[]
    for chunk in chucks: 
        if doc_type == chunk["document_type"]:
            paitent_data.append(chunk)

    return paitent_data




def decompose_query(query):

    query_lower = query.lower()

    # Step 1: Extract patient ID
    patient_match = re.search(
        r"patient\s+(P\d+)",
        query,
        re.IGNORECASE
    )

    patient_id = patient_match.group(1).upper() if patient_match else None

    # Step 2: Define query categories
    query_types = {
        "hba1c": {
            "keywords": ["hba1c", "blood sugar"],
            "document_types": ["lab_report"],
            "instruction": "Find HbA1c results and identify the latest record."
        },
        "medications": {
            "keywords": ["medication", "medications", "medicine",
                         "medicines", "prescribed"],
            "document_types": ["prescription"],
            "instruction": "Find prescribed medications."
        },
        "allergies": {
            "keywords": ["allergy", "allergies", "allergic"],
            "document_types": ["consultation"],
            "instruction": "Find reported allergies."
        },
        "imaging": {
            "keywords": ["x-ray", "xray", "imaging", "scan"],
            "document_types": ["imaging"],
            "instruction": "Find relevant imaging reports."
        }
    }

    # Step 3: Create sub-queries
    sub_queries = []

    for category, details in query_types.items():

        if any(keyword in query_lower
               for keyword in details["keywords"]):

            sub_queries.append({
                "category": category,
                "query": details["instruction"],
                "patient_id": patient_id,
                "document_types": details["document_types"]
            })

    # Step 4: Return decomposed query
    return {
        "original_query": query,
        "patient_id": patient_id,
        "sub_queries": sub_queries
    }





    