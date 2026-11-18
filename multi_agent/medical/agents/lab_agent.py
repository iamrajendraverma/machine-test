from multi_agent.medical.data import lab_records


def lab_agent(patient_id, test_name):
    """Return the patient's authorised lab records, newest first.

    test_name=None returns every authorised lab test for the patient.
    """
    matches = [
        report for report in lab_records
        if report["patient_id"] == patient_id
        and report["is_authorized"]
        and (test_name is None or report["test_name"] == test_name)
    ]
    return sorted(matches, key=lambda r: r["record_date"], reverse=True)
