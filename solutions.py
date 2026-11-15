from datetime import date

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
def detect_conflicts(chunks):
    conflicts = []

    grouped_chunks = {}

    for chunk in chunks:
        document_id = chunk["document_id"]

        grouped_chunks.setdefault(document_id, []).append(chunk)

    for document_id, document_chunks in grouped_chunks.items():

        for i in range(len(document_chunks)):
            for j in range(i + 1, len(document_chunks)):

                content_1 = document_chunks[i]["content"].lower()
                content_2 = document_chunks[j]["content"].lower()

                if content_1 != content_2:
                    conflicts.append({
                        "document_id": document_id,
                        "statement_1": content_1,
                        "statement_2": content_2,
                        "source_1": document_chunks[i]["source"],
                        "source_2": document_chunks[j]["source"]
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
