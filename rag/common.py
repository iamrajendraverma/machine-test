"""Helpers shared by the policy and medical pipelines."""


def dedupe(chunks, key_fields):
    """Keep the first chunk for each distinct combination of ``key_fields``."""
    seen = set()
    unique = []
    for chunk in chunks:
        key = tuple(chunk[field] for field in key_fields)
        if key not in seen:
            seen.add(key)
            unique.append(chunk)
    return unique


def rank_by_similarity(chunks):
    """Return chunks sorted by ``similarity_score``, highest first."""
    return sorted(chunks, key=lambda chunk: chunk["similarity_score"], reverse=True)


def top_k(chunks, k=3):
    return chunks[:k]
