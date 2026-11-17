from datetime import date

from rag.medical.data import chunks
from rag.medical.pipeline import EVIDENCE_FIELDS, medical_result
from tests.helpers import make_medical_chunk

EVAL = date(2026, 11, 14)
HBA1C_QUERY = "Show the latest HbA1c result for patient P001"


def test_latest_hba1c_for_p001_is_the_november_record():
    result = medical_result(HBA1C_QUERY, records=chunks, evaluation_date=EVAL)
    assert result["patient_id"] == "P001"
    assert result["warning"] is None
    assert len(result["evidence"]) == 1
    assert result["evidence"][0]["document_id"] == "DOC112"
    assert result["evidence"][0]["record_date"] == "2026-11-02"


def test_future_dated_record_never_returned():
    result = medical_result(HBA1C_QUERY, records=chunks, evaluation_date=date(2026, 6, 30))
    assert result["evidence"][0]["document_id"] == "DOC102"


def test_unauthorized_copy_cannot_shadow_authorized_one():
    records = [
        make_medical_chunk(document_id="DOC1", chunk_id="C1", document_type="lab_report",
                           record_date="2026-01-10", is_authorized=True, content="authorised"),
        make_medical_chunk(document_id="DOC1", chunk_id="C1", document_type="lab_report",
                           record_date="2026-01-10", is_authorized=False, content="unauthorised"),
    ]
    result = medical_result(HBA1C_QUERY, records=records, evaluation_date=EVAL)
    assert len(result["evidence"]) == 1
    assert result["evidence"][0]["content"] == "authorised"
    assert result["warning"] is None


def test_unauthorized_only_record_gives_no_evidence():
    records = [make_medical_chunk(document_id="DOC1", document_type="lab_report",
                                  record_date="2026-01-10", is_authorized=False)]
    result = medical_result(HBA1C_QUERY, records=records, evaluation_date=EVAL)
    assert result["evidence"] == []
    assert result["warning"] == "No evidence"


def test_no_patient_id_warning():
    result = medical_result("Show the latest HbA1c", records=chunks, evaluation_date=EVAL)
    assert result["patient_id"] is None
    assert result["warning"] == "No patient ID found in query"


def test_query_not_understood_warning():
    result = medical_result("What is the weather for patient P001?", records=chunks, evaluation_date=EVAL)
    assert result["patient_id"] == "P001"
    assert result["warning"] == "Query not understood"
    assert result["evidence"] == []


def test_evidence_contains_only_projected_fields():
    result = medical_result("patient P001 medications", records=chunks, evaluation_date=EVAL)
    assert result["evidence"]
    for item in result["evidence"]:
        assert set(item) == set(EVIDENCE_FIELDS)


def test_medication_query_returns_only_authorised_prescription():
    result = medical_result("patient P001 medications", records=chunks, evaluation_date=EVAL)
    assert [e["document_id"] for e in result["evidence"]] == ["DOC104"]


def test_default_evaluation_date_uses_today_without_error():
    result = medical_result(HBA1C_QUERY, records=chunks)
    assert result["patient_id"] == "P001"
