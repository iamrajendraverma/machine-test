import os
import sys
import unittest
from datetime import date

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from policy_data import chunks  # noqa: E402
from policy_management import (  # noqa: E402
    detect_conflicts,
    filter_effective_chunks,
    get_top_evidence,
    rank_chunks,
    remove_duplicates,
    retain_latest_policy_version,
)

EVALUATION_DATE = date(2026, 11, 14)


def make_chunk(document_id, chunk_id, policy_version=1, effective_date="2026-01-01",
               similarity_score=0.5, content="sample content", source="Policy_X"):
    return {
        "document_id": document_id,
        "chunk_id": chunk_id,
        "policy_version": policy_version,
        "effective_date": effective_date,
        "source": source,
        "similarity_score": similarity_score,
        "content": content,
    }


def keys(items):
    return [(c["document_id"], c["chunk_id"], c["policy_version"]) for c in items]


class RemoveDuplicatesTest(unittest.TestCase):

    def test_exact_duplicate_is_removed(self):
        result = remove_duplicates(chunks)
        self.assertEqual(len(result), len(chunks) - 1)
        self.assertEqual(len(keys(result)), len(set(keys(result))))

    def test_only_one_copy_of_POL001_C1_remains(self):
        result = remove_duplicates(chunks)
        matches = [c for c in result if c["document_id"] == "POL001" and c["chunk_id"] == "C1"]
        self.assertEqual(len(matches), 1)

    def test_same_chunk_id_with_different_version_is_kept(self):
        data = [
            make_chunk("POL100", "C1", policy_version=1),
            make_chunk("POL100", "C1", policy_version=2),
        ]
        self.assertEqual(len(remove_duplicates(data)), 2)

    def test_empty_input_returns_empty_list(self):
        self.assertEqual(remove_duplicates([]), [])

    def test_does_not_modify_input(self):
        data = [make_chunk("POL100", "C1"), make_chunk("POL100", "C1")]
        original_len = len(data)
        remove_duplicates(data)
        self.assertEqual(len(data), original_len)


class FilterEffectiveChunksTest(unittest.TestCase):

    def test_future_dated_chunks_are_excluded(self):
        result = filter_effective_chunks(chunks, EVALUATION_DATE)
        excluded = {(c["document_id"], c["chunk_id"]) for c in chunks} - \
                   {(c["document_id"], c["chunk_id"]) for c in result}
        self.assertIn(("POL002", "C3"), excluded)
        self.assertIn(("POL010", "C13"), excluded)

    def test_chunk_effective_on_evaluation_date_is_included(self):
        result = filter_effective_chunks(chunks, EVALUATION_DATE)
        ids = {(c["document_id"], c["chunk_id"]) for c in result}
        self.assertIn(("POL009", "C11"), ids)

    def test_chunk_effective_before_evaluation_date_is_included(self):
        result = filter_effective_chunks(chunks, EVALUATION_DATE)
        ids = {(c["document_id"], c["chunk_id"]) for c in result}
        self.assertIn(("POL001", "C2"), ids)

    def test_empty_input_returns_empty_list(self):
        self.assertEqual(filter_effective_chunks([], EVALUATION_DATE), [])

    def test_all_future_returns_empty(self):
        data = [make_chunk("POL100", "C1", effective_date="2030-01-01")]
        self.assertEqual(filter_effective_chunks(data, EVALUATION_DATE), [])


class RetainLatestPolicyVersionTest(unittest.TestCase):

    def pipeline(self, data):
        return retain_latest_policy_version(
            filter_effective_chunks(remove_duplicates(data), EVALUATION_DATE)
        )

    def test_only_latest_effective_version_is_kept(self):
        result = self.pipeline(chunks)
        pol001 = [c["chunk_id"] for c in result if c["document_id"] == "POL001"]
        self.assertEqual(pol001, ["C2"])

    def test_future_newer_version_is_ignored_and_older_effective_version_kept(self):
        result = self.pipeline(chunks)
        pol010 = [(c["chunk_id"], c["policy_version"]) for c in result if c["document_id"] == "POL010"]
        self.assertEqual(pol010, [("C12", 1)])

    def test_single_version_document_is_kept(self):
        result = self.pipeline(chunks)
        pol003 = [c["chunk_id"] for c in result if c["document_id"] == "POL003"]
        self.assertEqual(pol003, ["C4"])

    def test_empty_input_returns_empty_list(self):
        self.assertEqual(retain_latest_policy_version([]), [])


class RankChunksTest(unittest.TestCase):

    def test_sorted_by_similarity_descending(self):
        scores = [c["similarity_score"] for c in rank_chunks(chunks)]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_highest_score_is_first(self):
        self.assertEqual(rank_chunks(chunks)[0]["similarity_score"], 0.99)

    def test_does_not_modify_input_order(self):
        before = keys(chunks)
        rank_chunks(chunks)
        self.assertEqual(keys(chunks), before)


class DetectConflictsTest(unittest.TestCase):

    def test_identical_content_is_not_a_conflict(self):
        data = [
            make_chunk("POL100", "C1", content="Same statement."),
            make_chunk("POL100", "C2", content="Same statement."),
        ]
        self.assertEqual(detect_conflicts(data), [])

    def test_conflict_between_different_policies_is_detected(self):
        # POL005 and POL006 are contradictory policies in sample.py
        data = [
            make_chunk("POL005", "C7", content="Cash withdrawals abroad are allowed.", source="Policy_E"),
            make_chunk("POL006", "C8", content="Cash withdrawals abroad are not allowed.", source="Policy_F"),
        ]
        conflicts = detect_conflicts(data)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["source_1"], "Policy_E")
        self.assertEqual(conflicts[0]["source_2"], "Policy_F")

    def test_conflicts_detected_in_sample_data(self):
        conflicts = detect_conflicts(chunks)
        pairs = {frozenset((c["source_1"], c["source_2"])) for c in conflicts}
        self.assertIn(frozenset(("Policy_E", "Policy_F")), pairs)
        self.assertIn(frozenset(("Policy_G", "Policy_H")), pairs)

    def test_empty_input_returns_no_conflicts(self):
        self.assertEqual(detect_conflicts([]), [])


class GetTopEvidenceTest(unittest.TestCase):

    def test_returns_top_three_by_default(self):
        self.assertEqual(len(get_top_evidence(rank_chunks(chunks))), 3)

    def test_custom_top_n(self):
        self.assertEqual(len(get_top_evidence(chunks, top_n=5)), 5)

    def test_fewer_chunks_than_top_n(self):
        data = [make_chunk("POL100", "C1")]
        self.assertEqual(len(get_top_evidence(data)), 1)

    def test_provenance_fields_present(self):
        evidence = get_top_evidence(rank_chunks(chunks))[0]
        for field in ("document_id", "chunk_id", "policy_version",
                      "effective_date", "source", "similarity_score", "content"):
            self.assertIn(field, evidence)

    def test_preserves_order(self):
        ranked = rank_chunks(chunks)
        evidence = get_top_evidence(ranked)
        self.assertEqual(
            [e["chunk_id"] for e in evidence],
            [c["chunk_id"] for c in ranked[:3]],
        )


if __name__ == "__main__":
    unittest.main()
