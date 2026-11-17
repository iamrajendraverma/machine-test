from datetime import date

from rag.common import rank_by_similarity
from rag.policy.data import chunks
from rag.policy.pipeline import EVIDENCE_FIELDS, get_top_evidence, retrieve_evidence
from tests.helpers import make_policy_chunk

EVALUATION_DATE = date(2026, 11, 14)


def test_retrieve_evidence_reports_counts():
    result = retrieve_evidence(chunks, EVALUATION_DATE)
    assert result["evaluation_date"] == "2026-11-14"
    assert result["total_input_chunks"] == len(chunks)
    assert result["unique_chunks"] == len(chunks) - 1
    assert result["effective_chunks"] <= result["unique_chunks"]
    assert result["latest_policy_chunks"] <= result["effective_chunks"]


def test_retrieve_evidence_flags_conflicts_with_warning():
    result = retrieve_evidence(chunks, EVALUATION_DATE)
    assert result["conflicts_detected"] is True
    assert result["warning"] == "WARNING: Conflicting policy evidence detected."
    assert result["conflicts"]


def test_retrieve_evidence_without_conflicts():
    data = [make_policy_chunk("POL100", "C1", content="Card payments are allowed.")]
    result = retrieve_evidence(data, EVALUATION_DATE)
    assert result["conflicts_detected"] is False
    assert result["conflicts"] == []
    assert result["warning"] == "No conflicting policy evidence detected."


def test_retrieve_evidence_excludes_future_versions():
    result = retrieve_evidence(chunks, EVALUATION_DATE)
    ids = {(e["document_id"], e["chunk_id"]) for e in result["top_evidence"]}
    assert ("POL002", "C3") not in ids
    assert ("POL010", "C13") not in ids


def test_top_evidence_is_top_three_ranked_by_similarity():
    result = retrieve_evidence(chunks, EVALUATION_DATE)
    scores = [e["similarity_score"] for e in result["top_evidence"]]
    assert len(scores) == 3
    assert scores == sorted(scores, reverse=True)


def test_top_evidence_has_provenance_fields():
    evidence = retrieve_evidence(chunks, EVALUATION_DATE)["top_evidence"][0]
    assert set(evidence) == set(EVIDENCE_FIELDS)


def test_get_top_evidence_custom_n_and_small_input():
    ranked = rank_by_similarity(chunks)
    assert len(get_top_evidence(ranked, top_n=5)) == 5
    assert len(get_top_evidence([make_policy_chunk()])) == 1
    assert [e["chunk_id"] for e in get_top_evidence(ranked)] == [c["chunk_id"] for c in ranked[:3]]
