from rag.policy.conflicts import contradicts, detect_conflicts
from rag.policy.data import chunks
from tests.helpers import make_policy_chunk


def test_identical_content_is_not_a_conflict():
    data = [make_policy_chunk("POL100", "C1", content="Same statement."),
            make_policy_chunk("POL100", "C2", content="Same statement.")]
    assert detect_conflicts(data) == []


def test_allowed_vs_not_allowed_is_a_conflict():
    data = [
        make_policy_chunk("POL005", "C7", content="Cash withdrawals abroad are allowed.", source="Policy_E"),
        make_policy_chunk("POL006", "C8", content="Cash withdrawals abroad are not allowed.", source="Policy_F"),
    ]
    conflicts = detect_conflicts(data)
    assert len(conflicts) == 1
    assert conflicts[0]["source_1"] == "Policy_E"
    assert conflicts[0]["source_2"] == "Policy_F"
    assert conflicts[0]["document_id_1"] == "POL005"


def test_sample_data_conflicts_are_found():
    pairs = {frozenset((c["source_1"], c["source_2"])) for c in detect_conflicts(chunks)}
    assert frozenset(("Policy_E", "Policy_F")) in pairs
    assert frozenset(("Policy_G", "Policy_H")) in pairs


def test_no_shared_subject_means_no_conflict():
    assert not contradicts("Cash withdrawals are allowed.", "Crypto purchases are prohibited.")


def test_single_shared_subject_token_is_not_enough():
    assert not contradicts("Cards are allowed.", "Cards are prohibited.")


def test_same_polarity_is_not_a_conflict():
    assert not contradicts("Cash withdrawals abroad are allowed.",
                           "Cash withdrawals abroad are permitted.")


def test_empty_input_returns_no_conflicts():
    assert detect_conflicts([]) == []
