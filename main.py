from solutions import rank_chunks
from solutions import retain_latest_policy_version
from solutions import remove_duplicates, filter_effective_chunks,detect_conflicts,get_top_evidence
from sample import chunks
from datetime import date
import json



def main():
    EVALUATION_DATE = date(2026, 11, 14)

    result =retrieve_evidence(chunks,EVALUATION_DATE)
    
    print(json.dumps(result, indent=4))

    

def retrieve_evidence(chunks, evaluation_date):

    # 1. Remove duplicates
    unique_chunks = remove_duplicates(chunks)

    # 2. Filter future policies
    effective_chunks = filter_effective_chunks(
        unique_chunks,
        evaluation_date
    )

    # 3. Retain latest policy version
    latest_chunks = retain_latest_policy_version(effective_chunks)

    # 4. Detect conflicts
    conflicts = detect_conflicts(latest_chunks)

    # 5. Rank by similarity
    ranked_chunks = rank_chunks(latest_chunks)

    # 6. Get top three evidence chunks
    top_evidence = get_top_evidence(ranked_chunks, top_n=3)

    # 7. Generate explicit warning
    if conflicts:
        warning = "WARNING: Conflicting policy evidence detected."
    else:
        warning = "No conflicting policy evidence detected."

    return {
        "evaluation_date": evaluation_date.isoformat(),
        "total_input_chunks": len(chunks),
        "unique_chunks": len(unique_chunks),
        "effective_chunks": len(effective_chunks),
        "latest_policy_chunks": len(latest_chunks),
        "conflicts_detected": len(conflicts) > 0,
        "conflicts": conflicts,
        "warning": warning,
        "top_evidence": top_evidence
    }


if __name__ == "__main__":
    main()
