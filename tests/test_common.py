from rag.common import dedupe, rank_by_similarity, top_k
from tests.helpers import make_policy_chunk


def test_dedupe_keeps_first_occurrence_and_order():
    a = make_policy_chunk("POL1", "C1", content="first")
    b = make_policy_chunk("POL1", "C1", content="second")
    c = make_policy_chunk("POL2", "C1")
    result = dedupe([a, b, c], ("document_id", "chunk_id"))
    assert result == [a, c]


def test_dedupe_uses_only_given_key_fields():
    a = make_policy_chunk("POL1", "C1", policy_version=1)
    b = make_policy_chunk("POL1", "C1", policy_version=2)
    assert len(dedupe([a, b], ("document_id", "chunk_id"))) == 1
    assert len(dedupe([a, b], ("document_id", "chunk_id", "policy_version"))) == 2


def test_dedupe_empty_input():
    assert dedupe([], ("document_id",)) == []


def test_rank_by_similarity_is_descending_and_non_mutating():
    chunks = [make_policy_chunk(similarity_score=s) for s in (0.2, 0.9, 0.5)]
    before = list(chunks)
    scores = [c["similarity_score"] for c in rank_by_similarity(chunks)]
    assert scores == [0.9, 0.5, 0.2]
    assert chunks == before


def test_top_k_returns_at_most_k():
    assert top_k([1, 2, 3, 4], 2) == [1, 2]
    assert top_k([1, 2], 5) == [1, 2]
    assert top_k([], 3) == []
