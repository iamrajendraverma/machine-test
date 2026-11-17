"""Heuristic detection of contradicting policy statements.

Two statements conflict when they share at least ``MIN_SHARED_SUBJECT_TOKENS``
subject words and one is restrictive while the other is permissive.
"""

import re

STOPWORDS = {
    "a", "an", "the", "are", "is", "be", "must", "with", "without", "up",
    "to", "above", "below", "within", "by", "for", "of", "on", "in", "and",
    "or", "at", "than",
}
PERMISSIVE_WORDS = {"allowed", "permitted", "approved", "always"}
RESTRICTIVE_WORDS = {"not", "prohibited", "require", "requires", "required"}
MIN_SHARED_SUBJECT_TOKENS = 2


def _tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def _subject_tokens(tokens):
    """Words saying what the statement is about, without filler, polarity or numbers."""
    return {
        token for token in tokens
        if token not in STOPWORDS
        and token not in PERMISSIVE_WORDS
        and token not in RESTRICTIVE_WORDS
        and not token.isdigit()
    }


def _polarity(tokens):
    token_set = set(tokens)
    if token_set & RESTRICTIVE_WORDS:
        return "restrictive"
    if token_set & PERMISSIVE_WORDS:
        return "permissive"
    return None


def contradicts(text_a, text_b):
    tokens_a, tokens_b = _tokens(text_a), _tokens(text_b)

    shared_subject = _subject_tokens(tokens_a) & _subject_tokens(tokens_b)
    if len(shared_subject) < MIN_SHARED_SUBJECT_TOKENS:
        return False

    polarity_a, polarity_b = _polarity(tokens_a), _polarity(tokens_b)
    return (
        polarity_a is not None
        and polarity_b is not None
        and polarity_a != polarity_b
    )


def detect_conflicts(chunks):
    conflicts = []
    for i in range(len(chunks)):
        for j in range(i + 1, len(chunks)):
            chunk_1, chunk_2 = chunks[i], chunks[j]
            if contradicts(chunk_1["content"], chunk_2["content"]):
                conflicts.append({
                    "document_id_1": chunk_1["document_id"],
                    "document_id_2": chunk_2["document_id"],
                    "statement_1": chunk_1["content"],
                    "statement_2": chunk_2["content"],
                    "source_1": chunk_1["source"],
                    "source_2": chunk_2["source"],
                })
    return conflicts
