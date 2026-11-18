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


---

# 3. Machine Test 1: LangGraph – Healthcare Multi-Agent System

**Difficulty:** Senior  
**Round:** Python live coding + Senior AI/ML Engineer / Agentic AI Engineer interview  
**Stack:** Python, LangGraph, TypedDict, LLM/tool integrations

## Problem statement

A healthcare organization wants to build an AI-powered Patient Assistance System using LangGraph. The system helps authorized doctors retrieve information from patient medical records, analyze the retrieved evidence, validate the results, and generate a grounded response.

A doctor may ask:

> Find the latest HbA1c result for patient P001, check their diabetes medication, and summarize their health condition.

The system must understand the request, break it into smaller tasks, route each task to the appropriate specialist agent, collect the results, validate the evidence, and prepare a final response. It must not expose records belonging to another patient or invent information that is not present in the retrieved records.

## Required agents / graph nodes

| Agent / node | Responsibility |
| --- | --- |
| Query Agent | Understand the original request, extract the patient ID, and decompose the request into structured subqueries |
| Lab Agent | Retrieve relevant laboratory reports, including HbA1c results |
| Medication Agent | Retrieve medication and prescription information |
| Analysis Agent | Analyze the retrieved information and organize relevant findings |
| Validation Agent | Check evidence completeness, relevance, consistency, and provenance |
| Response Agent | Generate a concise, evidence-based response for the doctor |

You may implement each agent as a LangGraph node. The agents can call deterministic Python functions or mock tools for this machine test; an actual LLM integration is optional unless requested by the interviewer.

## Functional requirements

Implement a LangGraph workflow that:

1. Accepts the doctor's natural-language query.
2. Extracts the patient ID and decomposes the request into one or more structured subqueries.
3. Routes laboratory-related subqueries to the Lab Agent.
4. Routes medication-related subqueries to the Medication Agent.
5. Executes independent retrieval agents in parallel where appropriate.
6. Collects the results from all agents in shared graph state.
7. Combines the retrieved records into an evidence collection with source provenance.
8. Sends the evidence to the Validation Agent.
9. If validation succeeds, routes to the Response Agent.
10. If evidence is missing or invalid, attempts additional retrieval when appropriate, or returns an explicit insufficient-evidence response.
11. Returns the final response with the patient ID, findings, supporting evidence, and warnings.

## Shared state

Define a shared state using `TypedDict`. Include at least the following fields; you may add fields that are useful for routing, error handling, and auditability.

```python
from typing import TypedDict, Any

class AgentState(TypedDict, total=False):
    original_query: str
    patient_id: str
    sub_queries: list[dict[str, Any]]
    lab_results: list[dict[str, Any]]
    medication_results: list[dict[str, Any]]
    evidence: list[dict[str, Any]]
    validation_status: str
    validation_errors: list[str]
    retry_count: int
    final_response: str
    warnings: list[str]
```

For parallel branches, define appropriate state reducers or use another safe merge strategy so that concurrent node updates do not overwrite one another.

## Coding tasks

### Task 1 — Define the state

Create the `AgentState` schema using `TypedDict`. Decide which fields are required and which are optional. Include any additional fields needed to track errors, retries, and evidence provenance.

### Task 2 — Implement the agent nodes

Implement functions with signatures similar to the following:

```python
def query_agent(state: AgentState) -> dict:
    ...

def lab_agent(state: AgentState) -> dict:
    ...

def medication_agent(state: AgentState) -> dict:
    ...

def analysis_agent(state: AgentState) -> dict:
    ...

def validation_agent(state: AgentState) -> dict:
    ...

def response_agent(state: AgentState) -> dict:
    ...
```

Each node should read from the shared state and return only the state updates it owns. Use mock retrieval data if no database or vector store is available.

### Task 3 — Build the LangGraph workflow

Use the following LangGraph building blocks:

- `StateGraph`
- `START`
- `END`
- `add_node()`
- `add_edge()`
- `add_conditional_edges()`
- `compile()`
- `invoke()`

Register all nodes and connect them to form the workflow.

### Task 4 — Implement conditional routing

Create routing logic that determines which retrieval agents should run based on the decomposed subqueries.

Examples:

- A query asking for HbA1c should route to the Lab Agent.
- A query asking about diabetes medication should route to the Medication Agent.
- A query asking for both should execute both retrieval branches.
- A query that does not require either source should not invoke unrelated retrieval agents.

### Task 5 — Implement evidence preparation

Combine the results from the retrieval agents into a consistent evidence structure. Each evidence item should retain relevant provenance, such as:

- patient ID
- document ID
- chunk ID
- document type
- record date
- source document
- retrieved content

Do not discard provenance when combining agent outputs.

### Task 6 — Validate and handle failures

The Validation Agent should check that:

- Evidence belongs to the requested patient.
- Retrieved records are authorized for the requesting doctor.
- Evidence is relevant to the requested subquery.
- Required evidence is present.
- Conflicting or incomplete information is identified.

Use conditional routing after validation. If validation fails, either retry the relevant retrieval branch with a bounded retry count or return a clear insufficient-evidence response. Avoid infinite loops.

### Task 7 — Generate the response

The Response Agent should use only validated evidence. It should distinguish between facts found in records and information that is unavailable. Include warnings for missing or conflicting evidence. Do not generate a diagnosis or treatment recommendation unsupported by the records.

### Task 8 — Compile and run

Compile the graph and invoke it with a sample input:

```python
initial_state = {
    "original_query": (
        "Find the latest HbA1c result for patient P001, "
        "check their diabetes medication, and summarize "
        "their health condition."
    ),
    "patient_id": "P001",
    "retry_count": 0,
    "warnings": [],
}

result = graph.invoke(initial_state)
print(result["final_response"])
```

Adapt the invocation to your completed state schema.

## Expected workflow

```text
START
  |
Query Agent
  |
Conditional routing
  |--------------------------|
  v                          v
Lab Agent              Medication Agent
  |                          |
  |---------- merge ---------|
             |
       Analysis Agent
             |
      Validation Agent
             |
       Conditional route
        /          \
  Valid evidence   Invalid / incomplete
       |                 |
       v           Retry retrieval
 Response Agent          |
       |            Retry limit reached
       v                 |
      END <--------------+
```

The Lab Agent and Medication Agent should run in parallel when both are needed. The graph must merge their state updates before analysis.

## Sample test cases

1. **Combined query:** Ask for the latest HbA1c and current diabetes medication. Both retrieval agents should run.
2. **Lab-only query:** Ask for the latest HbA1c result. Only the Lab Agent should run.
3. **Medication-only query:** Ask which diabetes medication was prescribed. Only the Medication Agent should run.
4. **Missing evidence:** The requested lab report does not exist. The system should return an explicit warning rather than inventing a value.
5. **Unauthorized record:** A retrieval tool returns a record for another patient or an unauthorized record. It must not reach the final response.
6. **Conflicting evidence:** Two relevant records contain inconsistent values. The system should flag the conflict and preserve provenance.
7. **Transient retrieval failure:** One agent encounters a temporary error. The workflow should retry within a configured limit or continue safely with clearly marked partial results where appropriate.
8. **Retry exhaustion:** Retrieval continues to fail. The graph should terminate with a structured error or insufficient-evidence response.

## Expected output structure

The exact wording may vary, but the result should contain the patient identifier, findings, evidence, validation status, and warnings. For example:

```json
{
  "patient_id": "P001",
  "validation_status": "valid",
  "findings": {
    "latest_hba1c": "7.2%",
    "medications": ["Metformin 500 mg"]
  },
  "evidence": [
    {
      "document_id": "DOC102",
      "document_type": "lab_report",
      "record_date": "2026-06-15",
      "source": "lab_june.pdf",
      "content": "Patient HbA1c level is 7.2%."
    }
  ],
  "warnings": [],
  "final_response": "The latest available HbA1c result is 7.2% ..."
}
```

This is an illustrative output shape, not a hardcoded answer. Your implementation must retrieve and validate the data before producing the response.

## Interview follow-up questions

1. What is the role of shared state in LangGraph?
2. What is the difference between a node, an edge, and a conditional edge?
3. How would you execute the Lab Agent and Medication Agent in parallel?
4. How do you merge state updates from parallel nodes without overwriting data?
5. What is a reducer in LangGraph, and when would you use one?
6. How would you implement retry logic without creating an infinite graph loop?
7. What is the difference between a supervisor architecture and a fixed LangGraph workflow?
8. How would you persist graph state and resume an interrupted workflow?
9. How would you implement human approval before a sensitive action?
10. How would you handle partial results when one agent fails but another succeeds?
11. How would you trace agent execution and debug incorrect routing?
12. How would you protect PHI and enforce patient-level authorization across all agents?

## Evaluation criteria

| Area | What will be evaluated |
| --- | --- |
| Python implementation | Correctness, readability, typing, modular node functions |
| LangGraph fundamentals | StateGraph, nodes, edges, conditional routing, compile, invoke |
| State management | Correct state updates, reducers, safe parallel merging |
| Agent orchestration | Clear responsibilities, routing, parallel execution, coordination |
| Evidence handling | Provenance, relevance, authorization, conflict detection |
| Reliability | Bounded retries, partial failures, graceful fallback |
| Testing | Happy path, missing data, unauthorized data, conflicts, failure cases |
| Production readiness | Checkpointing, observability, auditability, PHI protection |

**Healthcare safety note:** This exercise focuses on retrieval, orchestration, and evidence handling. A production system must enforce authorization server-side, protect PHI throughout the pipeline, audit record access, and keep clinical decisions under qualified clinician control.
