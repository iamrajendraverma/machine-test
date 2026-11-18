lab_records = [
    {
        "patient_id": "P001",
        "document_id": "DOC101",
        "chunk_id": "C1",
        "document_type": "lab_report",
        "test_name": "HbA1c",
        "record_date": "2026-01-10",
        "result": "7.8%",
        "source": "lab_january.pdf",
        "is_authorized": True
    },
    {
        "patient_id": "P001",
        "document_id": "DOC102",
        "chunk_id": "C2",
        "document_type": "lab_report",
        "test_name": "HbA1c",
        "record_date": "2026-06-15",
        "result": "7.2%",
        "source": "lab_june.pdf",
        "is_authorized": True
    },
    {
        "patient_id": "P002",
        "document_id": "DOC103",
        "chunk_id": "C3",
        "document_type": "lab_report",
        "test_name": "HbA1c",
        "record_date": "2026-06-20",
        "result": "6.5%",
        "source": "patient2_lab.pdf",
        "is_authorized": False
    }
]

medication_records = [
    {
        "patient_id": "P001",
        "document_id": "DOC201",
        "chunk_id": "C4",
        "document_type": "prescription",
        "medicine": "Metformin",
        "dosage": "500 mg",
        "record_date": "2026-07-01",
        "source": "prescription_july.pdf",
        "is_authorized": True
    },
    {
        "patient_id": "P001",
        "document_id": "DOC202",
        "chunk_id": "C5",
        "document_type": "prescription",
        "medicine": "Glimepiride",
        "dosage": "1 mg",
        "record_date": "2026-08-01",
        "source": "prescription_august.pdf",
        "is_authorized": True
    }
]