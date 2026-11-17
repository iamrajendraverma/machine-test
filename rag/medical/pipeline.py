"""End-to-end medical evidence retrieval."""

from datetime import date

from rag.common import rank_by_similarity, top_k
from rag.medical.data import chunks as DEFAULT_RECORDS
from rag.medical.filters import (
    filter_authorized,
    filter_by_document_type,
    filter_by_patient,
    filter_future_records,
    remove_duplicates,
)
from rag.medical.query import decompose_query

EVIDENCE_FIELDS = (
    "document_id",
    "chunk_id",
    "record_date",
    "source",
    "similarity_score",
    "content",
)


def medical_result(query, records=DEFAULT_RECORDS, evaluation_date=None):
    if evaluation_date is None:
        evaluation_date = date.today()

    decomposed = decompose_query(query)
    patient_id = decomposed["patient_id"]
    sub_queries = decomposed["sub_queries"]

    if patient_id is None:
        return _build_result(None, query, [], "No patient ID found in query")
    if not sub_queries:
        return _build_result(patient_id, query, [], "Query not understood")

    # Filter first, then dedupe, so an unauthorized copy cannot shadow an
    # authorized one and future-dated records never reach the answer.
    base = filter_by_patient(records, patient_id)
    base = filter_authorized(base)
    base = filter_future_records(base, evaluation_date)
    base = remove_duplicates(base)

    evidence = []
    for sub_query in sub_queries:
        matches = []
        for doc_type in sub_query["document_types"]:
            matches.extend(filter_by_document_type(base, doc_type))

        if sub_query["category"] == "hba1c":
            # "latest" questions want the most recent record, not the best match.
            matches = sorted(matches, key=lambda c: c["record_date"], reverse=True)[:1]
        else:
            matches = top_k(rank_by_similarity(matches))

        evidence.extend(matches)

    evidence = remove_duplicates(evidence)
    projected = [{field: chunk[field] for field in EVIDENCE_FIELDS} for chunk in evidence]

    warning = None if projected else "No evidence"
    return _build_result(patient_id, query, projected, warning)


def _build_result(patient_id, query, evidence, warning):
    return {
        "patient_id": patient_id,
        "query": query,
        "evidence": evidence,
        "warning": warning,
    }
