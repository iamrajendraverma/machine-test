"""Chunk factories shared by the test modules."""


def make_policy_chunk(document_id="POL100", chunk_id="C1", policy_version=1,
                      effective_date="2026-01-01", similarity_score=0.5,
                      content="sample content", source="Policy_X"):
    return {
        "document_id": document_id,
        "chunk_id": chunk_id,
        "policy_version": policy_version,
        "effective_date": effective_date,
        "source": source,
        "similarity_score": similarity_score,
        "content": content,
    }


def make_medical_chunk(patient_id="P001", document_id="DOC900", chunk_id="C1",
                       document_type="lab_report", record_date="2026-01-01",
                       similarity_score=0.5, source="record.pdf",
                       is_authorized=True, content="sample content"):
    return {
        "patient_id": patient_id,
        "document_id": document_id,
        "chunk_id": chunk_id,
        "document_type": document_type,
        "record_date": record_date,
        "similarity_score": similarity_score,
        "source": source,
        "is_authorized": is_authorized,
        "content": content,
    }


def policy_keys(items):
    return [(c["document_id"], c["chunk_id"], c["policy_version"]) for c in items]
