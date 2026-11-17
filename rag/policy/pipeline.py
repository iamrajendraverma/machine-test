"""End-to-end policy evidence retrieval."""

from rag.common import rank_by_similarity, top_k
from rag.policy.conflicts import detect_conflicts
from rag.policy.filters import (
    filter_effective_chunks,
    remove_duplicates,
    retain_latest_policy_version,
)

EVIDENCE_FIELDS = (
    "document_id",
    "chunk_id",
    "policy_version",
    "effective_date",
    "source",
    "similarity_score",
    "content",
)


def get_top_evidence(chunks, top_n=3):
    return [
        {field: chunk[field] for field in EVIDENCE_FIELDS}
        for chunk in top_k(chunks, top_n)
    ]


def retrieve_evidence(chunks, evaluation_date, top_n=3):
    unique_chunks = remove_duplicates(chunks)
    effective_chunks = filter_effective_chunks(unique_chunks, evaluation_date)
    latest_chunks = retain_latest_policy_version(effective_chunks)
    conflicts = detect_conflicts(latest_chunks)
    ranked_chunks = rank_by_similarity(latest_chunks)

    if conflicts:
        warning = "WARNING: Conflicting policy evidence detected."
    else:
        warning = "No conflicting policy evidence detected."

    return {
        "evaluation_date": evaluation_date.isoformat(),
        "total_input_chunks": len(chunks),
        "unique_chunks": len(unique_chunks),
        "effective_chunks": len(effective_chunks),
        "latest_policy_chunks": len(latest_chunks),
        "conflicts_detected": len(conflicts) > 0,
        "conflicts": conflicts,
        "warning": warning,
        "top_evidence": get_top_evidence(ranked_chunks, top_n),
    }
