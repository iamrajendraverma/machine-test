from datetime import date

from rag.policy.data import chunks
from rag.policy.filters import (
    filter_effective_chunks,
    remove_duplicates,
    retain_latest_policy_version,
)
from tests.helpers import make_policy_chunk, policy_keys

EVALUATION_DATE = date(2026, 11, 14)


def pipeline(data):
    return retain_latest_policy_version(
        filter_effective_chunks(remove_duplicates(data), EVALUATION_DATE)
    )


# remove_duplicates

def test_exact_duplicate_is_removed():
    result = remove_duplicates(chunks)
    assert len(result) == len(chunks) - 1
    assert len(policy_keys(result)) == len(set(policy_keys(result)))


def test_same_chunk_id_with_different_version_is_kept():
    data = [make_policy_chunk("POL100", "C1", policy_version=1),
            make_policy_chunk("POL100", "C1", policy_version=2)]
    assert len(remove_duplicates(data)) == 2


def test_remove_duplicates_empty_and_non_mutating():
    assert remove_duplicates([]) == []
    data = [make_policy_chunk(), make_policy_chunk()]
    remove_duplicates(data)
    assert len(data) == 2


# filter_effective_chunks

def test_future_dated_chunks_are_excluded():
    ids = {(c["document_id"], c["chunk_id"]) for c in filter_effective_chunks(chunks, EVALUATION_DATE)}
    assert ("POL002", "C3") not in ids
    assert ("POL010", "C13") not in ids


def test_chunk_effective_on_evaluation_date_is_included():
    ids = {(c["document_id"], c["chunk_id"]) for c in filter_effective_chunks(chunks, EVALUATION_DATE)}
    assert ("POL009", "C11") in ids


def test_chunk_effective_before_evaluation_date_is_included():
    ids = {(c["document_id"], c["chunk_id"]) for c in filter_effective_chunks(chunks, EVALUATION_DATE)}
    assert ("POL001", "C2") in ids


def test_all_future_returns_empty():
    data = [make_policy_chunk(effective_date="2030-01-01")]
    assert filter_effective_chunks(data, EVALUATION_DATE) == []


def test_filter_effective_empty_input():
    assert filter_effective_chunks([], EVALUATION_DATE) == []


# retain_latest_policy_version

def test_only_latest_effective_version_is_kept():
    assert [c["chunk_id"] for c in pipeline(chunks) if c["document_id"] == "POL001"] == ["C2"]


def test_future_newer_version_ignored_older_effective_version_kept():
    pol010 = [(c["chunk_id"], c["policy_version"]) for c in pipeline(chunks) if c["document_id"] == "POL010"]
    assert pol010 == [("C12", 1)]


def test_single_version_document_is_kept():
    assert [c["chunk_id"] for c in pipeline(chunks) if c["document_id"] == "POL003"] == ["C4"]


def test_retain_latest_empty_input():
    assert retain_latest_policy_version([]) == []
