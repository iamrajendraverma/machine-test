from policy_management import rank_chunks
from policy_management import retain_latest_policy_version
from policy_data import chunks
from datetime import date
import json
from medical_data import chunks as medical_data
from medical_management import remove_duplicates,filter_by_patient,filter_authorized,filter_future_records,rank_by_similarity,get_top_k,decompose_query,filter_by_document_type



def main():
    # EVALUATION_DATE = date(2026, 11, 14)

    # result =retrieve_evidence(policy_data,EVALUATION_DATE)

    # print(json.dumps(result, indent=4))
    # medical_pipeline(medical_data)
    query = "Show the latest HbA1c result for patient P001"

    query_decompositoon  = decompose_query(query)

    """
    INPUT
    {
    "original_query": "Show the latest HbA1c result for patient P001",
    "patient_id": "P001",
    "sub_queries": [
        {
            "category": "hba1c",
            "query": "Find HbA1c results and identify the latest record.",
            "patient_id": "P001",
            "document_types": [
                "lab_report"
            ]
        }
    ]
}
OUTPUT

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
    """
    query = "Show the latest HbA1c result for patient P001"
    output =medical_result(query)
    print(f" Output {json.dumps(output,indent=4)}")


def medical_pipeline(chunks):
   patients_record =remove_duplicates(chunks)
   print(f"Remove duplicate {len(patients_record)}")
   patient_record = filter_by_patient(patients_record,"P001")
   print(f"paitent data P001  {len(patient_record)}")
   authorized_paitent  = filter_authorized(patient_record)
   print(f"Authorized data  {len(authorized_paitent)}")
   cut_off_date  = date(2026,12,1)
   cut_off_data  = filter_future_records(authorized_paitent,cut_off_date)
   print(f"cut off data by date 2026/12/1 {len(cut_off_data)}")
   rank_chunks  = rank_by_similarity(cut_off_data)
   top_3  = get_top_k(rank_chunks)
   print(f" Top Three  {json.dumps(top_3,indent=4)}")


EVIDENCE_FIELDS = (
    "document_id",
    "chunk_id",
    "record_date",
    "source",
    "similarity_score",
    "content",
)


def medical_result(query, records=medical_data, evaluation_date=None):
    if evaluation_date is None:
        evaluation_date = date.today()

    decomposed = decompose_query(query)
    patient_id = decomposed["patient_id"]
    sub_queries = decomposed["sub_queries"]

    if patient_id is None:
        return _build_result(None, query, [], "No patient ID found in query")
    if not sub_queries:
        return _build_result(patient_id, query, [], "Query not understood")

    # Filter first, then dedupe, so an unauthorized copy cannot shadow an
    # authorized one and future-dated records never reach the answer.
    base = filter_by_patient(records, patient_id)
    base = filter_authorized(base)
    base = filter_future_records(base, evaluation_date)
    base = remove_duplicates(base)

    evidence = []
    for sub_query in sub_queries:
        matches = []
        for doc_type in sub_query["document_types"]:
            matches.extend(filter_by_document_type(base, doc_type))

        if sub_query["category"] == "hba1c":
            # "latest" questions want the most recent record, not the best match.
            matches = sorted(matches, key=lambda c: c["record_date"], reverse=True)[:1]
        else:
            matches = get_top_k(rank_by_similarity(matches))

        evidence.extend(matches)

    evidence = remove_duplicates(evidence)
    projected = [{field: chunk[field] for field in EVIDENCE_FIELDS} for chunk in evidence]

    warning = None if projected else "No evidence"
    return _build_result(patient_id, query, projected, warning)


def _build_result(patient_id, query, evidence, warning):
    return {
        "patient_id": patient_id,
        "query": query,
        "evidence": evidence,
        "warning": warning,
    }


# def retrieve_evidence(chunks, evaluation_date):

#     # 1. Remove duplicates
#     unique_chunks = remove_duplicates(chunks)

#     # 2. Filter future policies
#     effective_chunks = filter_effective_chunks(
#         unique_chunks,
#         evaluation_date
#     )

#     # 3. Retain latest policy version
#     latest_chunks = retain_latest_policy_version(effective_chunks)

#     # 4. Detect conflicts
#     conflicts = detect_conflicts(latest_chunks)

#     # 5. Rank by similarity
#     ranked_chunks = rank_chunks(latest_chunks)

#     # 6. Get top three evidence chunks
#     top_evidence = get_top_evidence(ranked_chunks, top_n=3)

#     # 7. Generate explicit warning
#     if conflicts:
#         warning = "WARNING: Conflicting policy evidence detected."
#     else:
#         warning = "No conflicting policy evidence detected."

#     return {
#         "evaluation_date": evaluation_date.isoformat(),
#         "total_input_chunks": len(chunks),
#         "unique_chunks": len(unique_chunks),
#         "effective_chunks": len(effective_chunks),
#         "latest_policy_chunks": len(latest_chunks),
#         "conflicts_detected": len(conflicts) > 0,
#         "conflicts": conflicts,
#         "warning": warning,
#         "top_evidence": top_evidence
#     }


if __name__ == "__main__":
    main()
