# AI/ML machine test

live coding round – Python

1.  Coding Challenge: Evidence-Aware Retrieval with Conflict Detection

deliot 

Problem statement:

You are developing a knowledge retrieval service for **AMEX**.

The system receives document chunks from multiple **policy versions**. Each chunk contains:

- document_id
- chunk_id
- policy_version
- effective_date
- source
- similarity_score
- content

The retrieval service may return **duplicate chunks**, **outdated policy versions** and **conflicting statements**.

Write a Python code that:

1. Removes duplicate chunks.
2. Excludes documents that are not yet effective.
3. Retains only the latest effective policy version for each document.
4. Ranks the remaining chunks by similarity score.
5. Identifies conflicting policy statements.
6. Returns the top three evidence chunks with their provenance.
7. Returns an explicit warning when conflicting evidence is detected.

Starter dataset

Python

from datetime import date

```json
chunks = [
{
"document_id": "POL001",
"chunk_id": "C1",
"policy_version": 1,
"effective_date": "2026-01-01",
"source": "Policy_A",
"similarity_score": 0.95,
"content": "International transactions require verification."
},
{
"document_id": "POL001",
"chunk_id": "C1",
"policy_version": 1,
"effective_date": "2026-01-01",
"source": "Policy_A",
"similarity_score": 0.95,
"content": "International transactions require verification."
},
{
"document_id": "POL001",
"chunk_id": "C2",
"policy_version": 2,
"effective_date": "2026-06-01",
"source": "Policy_B",
"similarity_score": 0.91,
"content": "International transactions require additional verification."
},
{
"document_id": "POL002",
"chunk_id": "C3",
"policy_version": 1,
"effective_date": "2027-01-01",
"source": "Future_Policy",
"similarity_score": 0.99,
"content": "All transactions require verification."
},
{
"document_id": "POL003",
"chunk_id": "C4",
"policy_version": 1,
"effective_date": "2026-01-01",
"source": "Policy_C",
"similarity_score": 0.88,
"content": "Domestic transactions require verification."
}
]
```

Use date(2026, 11, 14) as the evaluation date for this exercise.



---

# 2. Healthcare RAG: Patient Knowledge Assistant

**Difficulty:** Hard  
**Round:** Python live coding + Senior AI/ML Engineer / AI Solution Architect interview

## Problem statement

A healthcare organization wants to build an AI-powered assistant that helps authorized doctors retrieve relevant information from patient medical records.

The organization stores millions of documents, including:

- Patient medical history
- Lab reports
- Doctor consultation notes
- Prescription records
- Discharge summaries
- Radiology reports

Doctors may ask questions such as:

- What medications has this patient taken in the last six months?
- Does the patient have any recorded allergies?
- What was the patient's latest HbA1c result?
- Summarize the patient's medical history.
- Find lab reports related to kidney function.

Your task is to implement the evidence-retrieval layer of a RAG system. The service must return relevant, authorized, date-valid evidence with provenance. It must not expose another patient's records or imply facts that are not supported by the retrieved evidence.

## System requirements

Implement a Python retrieval pipeline that:

1. Removes duplicate chunks while preserving their original order.
2. Filters records to the requested patient ID.
3. Excludes records that the requesting user is not authorized to access.
4. Excludes future-dated medical records.
5. Ranks the remaining chunks by similarity score (highest first).
6. Returns the top three evidence chunks.
7. Includes source document, record date, patient ID, and document ID as provenance.
8. Returns an explicit warning when no usable evidence is found.
9. Does not generate a medical conclusion unsupported by the evidence.

**Important:** Do not automatically keep only the latest document across all medical records. Older records may be important medical history. Apply date and relevance filtering according to the user's question. For a question asking for the latest HbA1c result, the latest relevant lab evidence should be identified from the eligible records.

## Starter dataset

```python
from datetime import date

chunks = [
    {
        "patient_id": "P001",
        "document_id": "DOC101",
        "chunk_id": "C1",
        "document_type": "lab_report",
        "record_date": "2026-01-10",
        "similarity_score": 0.95,
        "source": "lab_january.pdf",
        "is_authorized": True,
        "content": "Patient HbA1c level is 7.8%."
    },
    {
        "patient_id": "P001",
        "document_id": "DOC101",
        "chunk_id": "C1",
        "document_type": "lab_report",
        "record_date": "2026-01-10",
        "similarity_score": 0.95,
        "source": "lab_january.pdf",
        "is_authorized": True,
        "content": "Patient HbA1c level is 7.8%."
    },
    {
        "patient_id": "P001",
        "document_id": "DOC102",
        "chunk_id": "C2",
        "document_type": "lab_report",
        "record_date": "2026-06-15",
        "similarity_score": 0.92,
        "source": "lab_june.pdf",
        "is_authorized": True,
        "content": "Patient HbA1c level is 7.2%."
    },
    {
        "patient_id": "P002",
        "document_id": "DOC103",
        "chunk_id": "C3",
        "document_type": "lab_report",
        "record_date": "2026-06-20",
        "similarity_score": 0.99,
        "source": "patient2_lab.pdf",
        "is_authorized": False,
        "content": "Patient HbA1c level is 6.5%."
    },
    {
        "patient_id": "P001",
        "document_id": "DOC104",
        "chunk_id": "C4",
        "document_type": "prescription",
        "record_date": "2026-07-01",
        "similarity_score": 0.88,
        "source": "prescription_july.pdf",
        "is_authorized": True,
        "content": "Patient was prescribed Metformin 500 mg."
    },
    {
        "patient_id": "P001",
        "document_id": "DOC105",
        "chunk_id": "C5",
        "document_type": "consultation",
        "record_date": "2026-08-01",
        "similarity_score": 0.85,
        "source": "doctor_notes.pdf",
        "is_authorized": True,
        "content": "Patient reported an allergy to Penicillin."
    },
    {
        "patient_id": "P001",
        "document_id": "DOC106",
        "chunk_id": "C6",
        "document_type": "lab_report",
        "record_date": "2027-01-10",
        "similarity_score": 0.98,
        "source": "future_lab.pdf",
        "is_authorized": True,
        "content": "Patient HbA1c level is 6.1%."
    }
]
```

**Evaluation date:** `date(2026, 11, 16)`  
**User query:** `What is the patient's latest HbA1c result?`  
**Patient ID:** `P001`

## Coding tasks

Create the following functions (you may choose suitable function signatures):

1. `remove_duplicates(chunks)` — remove duplicate chunks and preserve order.
2. `filter_by_patient(chunks, patient_id)` — retain only the requested patient's records.
3. `filter_authorized(chunks)` — exclude records that are not authorized.
4. `filter_future_records(chunks, evaluation_date)` — exclude records dated after the evaluation date.
5. `rank_by_similarity(chunks)` — sort eligible chunks by similarity score, descending.
6. `get_top_k(chunks, k=3)` — return the top K evidence chunks.
7. `build_evidence_response(chunks, patient_id, query)` — return evidence with provenance and an explicit warning when no evidence is available.

You may implement a single orchestration function to call these steps in a safe, documented order.

## Expected output structure

The response should follow this general structure (the example shows one evidence item; the implementation should return up to three eligible evidence chunks):

```json
{
  "patient_id": "P001",
  "query": "What is the patient's latest HbA1c result?",
  "evidence": [
    {
      "document_id": "DOC102",
      "chunk_id": "C2",
      "record_date": "2026-06-15",
      "source": "lab_june.pdf",
      "similarity_score": 0.92,
      "content": "Patient HbA1c level is 7.2%."
    }
  ],
  "warning": null
}
```

The example is illustrative, not a hardcoded answer. Your code must implement all filtering, ranking, and top-K requirements.

## Interview follow-up questions

1. Why must patient authorization and patient-ID filtering happen before retrieved context is sent to the LLM?
2. What is the difference between metadata filtering and semantic search?
3. How would you handle two lab reports with different HbA1c values?
4. How would you prevent the LLM from inventing a medical result?
5. How would you protect PHI in embeddings, vector databases, logs, and model prompts?
6. What should the system do when retrieval returns no relevant evidence?
7. How would you evaluate retrieval quality and answer faithfulness?
8. How would you scale this system to ten million medical documents?
9. How would you implement hybrid retrieval (BM25 + vector search) and reranking?
10. How would you audit which records were accessed and which evidence supported an answer?

## Evaluation criteria

- Python correctness and readable function design
- Deduplication and edge-case handling
- Secure patient-level metadata filtering and authorization
- Correct date parsing and future-record exclusion
- Similarity ranking and top-K selection
- Evidence provenance and explicit abstention
- Understanding of RAG security, evaluation, and production architecture

**Healthcare safety note:** This exercise is about retrieval and evidence handling, not diagnosis or treatment recommendations. A production system must enforce authorization server-side, protect PHI throughout the pipeline, and require clinician judgment for medical decisions.
