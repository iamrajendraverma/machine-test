from rag.medical.query import decompose_query, extract_patient_id


def test_patient_id_extracted_and_uppercased():
    assert extract_patient_id("show records for patient p001") == "P001"


def test_missing_patient_id_is_none():
    assert extract_patient_id("show the latest HbA1c") is None


def test_hba1c_query_maps_to_lab_report():
    result = decompose_query("Show the latest HbA1c result for patient P001")
    assert result["patient_id"] == "P001"
    assert len(result["sub_queries"]) == 1
    sub = result["sub_queries"][0]
    assert sub["category"] == "hba1c"
    assert sub["document_types"] == ["lab_report"]
    assert sub["patient_id"] == "P001"


def test_each_category_keyword_is_recognised():
    cases = {
        "medication": "medications",
        "which medicines were prescribed": "medications",
        "any allergies?": "allergies",
        "chest x-ray results": "imaging",
        "blood sugar trend": "hba1c",
    }
    for query, category in cases.items():
        categories = [s["category"] for s in decompose_query(query)["sub_queries"]]
        assert category in categories, query


def test_multi_category_query_yields_several_sub_queries():
    query = "patient P001 HbA1c and allergies and imaging"
    categories = {s["category"] for s in decompose_query(query)["sub_queries"]}
    assert categories == {"hba1c", "allergies", "imaging"}


def test_unknown_query_has_no_sub_queries():
    result = decompose_query("What is the weather today?")
    assert result["sub_queries"] == []
    assert result["original_query"] == "What is the weather today?"
