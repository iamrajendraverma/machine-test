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

## Let's create the answer with out code 


 1. Removes duplicate chunks.

 ```json 
 chunks = [{
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
 2. Excludes documents that are not yet effective.

  ```json 
 chunks = [{
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
},{
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

 3. Retains only the latest effective policy version for each document.

   ```json 
 chunks = [
{
"document_id": "POL001",
"chunk_id": "C2",
"policy_version": 2,
"effective_date": "2026-06-01",
"source": "Policy_B",
"similarity_score": 0.91,
"content": "International transactions require additional verification."
},{
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

  4. Ranks the remaining chunks by similarity score.

  
```json 
 chunks = [
{
"document_id": "POL001",
"chunk_id": "C2",
"policy_version": 2,
"effective_date": "2026-06-01",
"source": "Policy_B",
"similarity_score": 0.91,
"content": "International transactions require additional verification."
},{
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
 5. Identifies conflicting policy statements.

 - No conflicts 
 6. Returns the top three evidence chunks with their provenance.
  - No find 
  7.  Returns an explicit warning when conflicting evidence is detected.

  ```json 
{
    "evaluation_date": "2026-11-14",
    "total_input_chunks": 5,
    "unique_chunks": 4,
    "effective_chunks": 3,
    "latest_policy_chunks": 2,
    "conflicts_detected": false,
    "conflicts": [],
    "warning": "No conflicting policy evidence detected.",
    "top_evidence": [
        {
            "document_id": "POL001",
            "chunk_id": "C2",
            "policy_version": 2,
            "effective_date": "2026-11-01",
            "source": "Policy_B",
            "similarity_score": 0.91,
            "content": "International transactions require additional verification."
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
}
``` 

