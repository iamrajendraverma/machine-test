from multi_agent.medical.data import medication_records


def medication_agent(patient_id):
    """Return the patient's authorised prescriptions, newest first."""
    matches = [
        record for record in medication_records
        if record["patient_id"] == patient_id and record["is_authorized"]
    ]
    return sorted(matches, key=lambda r: r["record_date"], reverse=True)
