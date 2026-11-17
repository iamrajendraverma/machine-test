"""Pure filters over medical record chunks."""

from datetime import date

from rag.common import dedupe

MEDICAL_KEY_FIELDS = ("patient_id", "document_id", "chunk_id")


def remove_duplicates(chunks):
    return dedupe(chunks, MEDICAL_KEY_FIELDS)


def filter_by_patient(chunks, patient_id):
    return [chunk for chunk in chunks if chunk["patient_id"] == patient_id]


def filter_authorized(chunks):
    return [chunk for chunk in chunks if chunk["is_authorized"]]


def filter_future_records(chunks, evaluation_date: date):
    """Keep records dated on or before ``evaluation_date``."""
    return [
        chunk for chunk in chunks
        if date.fromisoformat(chunk["record_date"]) <= evaluation_date
    ]


def filter_by_document_type(chunks, doc_type):
    return [chunk for chunk in chunks if chunk["document_type"] == doc_type]
