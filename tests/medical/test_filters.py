from datetime import date

from rag.medical.filters import (
    filter_authorized,
    filter_by_document_type,
    filter_by_patient,
    filter_future_records,
    remove_duplicates,
)
from rag.medical.data import chunks
from tests.helpers import make_medical_chunk


def test_filter_by_patient_isolates_records():
    result = filter_by_patient(chunks, "P002")
    assert result and all(c["patient_id"] == "P002" for c in result)


def test_filter_by_patient_unknown_returns_empty():
    assert filter_by_patient(chunks, "P999") == []


def test_filter_authorized_drops_unauthorized_copy():
    p001 = filter_by_patient(chunks, "P001")
    authorized = filter_authorized(p001)
    assert all(c["is_authorized"] for c in authorized)
    assert len(authorized) == len(p001) - 2  # DOC101 unauthorised copy, DOC111 unauthorised


def test_future_records_excluded_and_boundary_included():
    p001 = filter_by_patient(chunks, "P001")
    dates = {c["record_date"] for c in filter_future_records(p001, date(2026, 11, 14))}
    assert "2027-01-10" not in dates          # DOC106 is in the future
    assert "2026-11-02" in dates               # DOC112 is before the cut-off
    boundary = [make_medical_chunk(record_date="2026-11-14")]
    assert len(filter_future_records(boundary, date(2026, 11, 14))) == 1


def test_filter_by_document_type():
    result = filter_by_document_type(chunks, "prescription")
    assert result and all(c["document_type"] == "prescription" for c in result)


def test_remove_duplicates_key_includes_patient_id():
    a = make_medical_chunk(patient_id="P001", chunk_id="C1")
    b = make_medical_chunk(patient_id="P002", chunk_id="C1")
    assert len(remove_duplicates([a, b])) == 2


def test_remove_duplicates_removes_same_patient_document_chunk():
    result = remove_duplicates(chunks)
    assert len(result) == len(chunks) - 1
