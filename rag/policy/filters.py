"""Pure filters over policy chunks."""

from datetime import date

from rag.common import dedupe

POLICY_KEY_FIELDS = ("document_id", "chunk_id", "policy_version")


def remove_duplicates(chunks):
    return dedupe(chunks, POLICY_KEY_FIELDS)


def filter_effective_chunks(chunks, evaluation_date: date):
    """Keep chunks whose ``effective_date`` is on or before ``evaluation_date``."""
    return [
        chunk for chunk in chunks
        if date.fromisoformat(chunk["effective_date"]) <= evaluation_date
    ]


def retain_latest_policy_version(chunks):
    """Keep only chunks whose version is the highest seen for their document."""
    latest_versions = {}
    for chunk in chunks:
        document_id = chunk["document_id"]
        version = chunk["policy_version"]
        if document_id not in latest_versions or version > latest_versions[document_id]:
            latest_versions[document_id] = version

    return [
        chunk for chunk in chunks
        if chunk["policy_version"] == latest_versions[chunk["document_id"]]
    ]
