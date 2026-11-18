Input 
```python 
query = "Find the latest HbA1c result and diabetes medication for patient P001"
```
Expect Out 

```json 
{
    "patient_id": "P001",
    "sub_queries": [
        {
            "category": "lab",
            "query": "Find the latest HbA1c result"
        },
        {
            "category": "medication",
            "query": "Find diabetes medication"
        }
    ]
}
```
2. Design the Query Agent

```text 
Input: Natural-language query

Doctor's question
      |
Step 1: Extract patient ID

Extract P001.
      |
Step 2: Identify intent

Identify lab and medication requirements.
      |

Step 3: Decompose query

Create independent structured subqueries.
      |

Output: Structured data

Patient ID + subqueries
```
