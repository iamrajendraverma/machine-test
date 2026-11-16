from datetime import date
import re


def remove_duplicates(chunks):
    seen = set()
    unique_chunks = []

    for chuck in chunks:
        key = (chuck["document_id"], chuck["chunk_id"],chuck["policy_version"])
        if key not in seen:
            seen.add(key)
            unique_chunks.append(chuck)

    return unique_chunks

def filter_effective_chunks(chunks, evaluation_date):
    effective_chunks = []

    for chunk in chunks:
        policy_date = date.fromisoformat(chunk["effective_date"])

        if policy_date <= evaluation_date:
            effective_chunks.append(chunk)

    return effective_chunks

def retain_latest_policy_version(chunks):
    latest_versions = {}

    for chunk in chunks:
        document_id = chunk["document_id"]
        version = chunk["policy_version"]

        if (
            document_id not in latest_versions
            or version > latest_versions[document_id]
        ):
            latest_versions[document_id] = version

    result = []

    for chunk in chunks:
        if chunk["policy_version"] == latest_versions[chunk["document_id"]]:
            result.append(chunk)

    return result
def rank_chunks(chunks):
    return sorted(
        chunks,
        key=lambda chunk: chunk["similarity_score"],
        reverse=True
    )
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
    # Words that say what the statement is about (e.g. "cash withdrawals
    # abroad"), without filler, polarity words or numbers.
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

#  This function checks two things:
# - Do both statements talk about the same subject?
# - Do they have opposite meanings according to the polarity rules?
def _contradicts(text_a, text_b):
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

            if _contradicts(chunk_1["content"], chunk_2["content"]):
                conflicts.append({
                    "document_id_1": chunk_1["document_id"],
                    "document_id_2": chunk_2["document_id"],
                    "statement_1": chunk_1["content"],
                    "statement_2": chunk_2["content"],
                    "source_1": chunk_1["source"],
                    "source_2": chunk_2["source"]
                })

    return conflicts
def get_top_evidence(chunks, top_n=3):
    evidence = []

    for chunk in chunks[:top_n]:
        evidence.append({
            "document_id": chunk["document_id"],
            "chunk_id": chunk["chunk_id"],
            "policy_version": chunk["policy_version"],
            "effective_date": chunk["effective_date"],
            "source": chunk["source"],
            "similarity_score": chunk["similarity_score"],
            "content": chunk["content"]
        })

    return evidence
