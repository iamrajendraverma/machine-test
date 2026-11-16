# Plan: make `detect_conflicts` find real contradictions

## Context

Question: why does `detect_conflicts` in `solutions.py` use `if content_1 != content_2`?

Answer: it is a placeholder heuristic. The author grouped chunks by `document_id`
and assumed that two chunks in the same document with different text contradict each other.
`!=` only says "the text differs", not "the statements contradict". `.lower()` just avoids
case-only differences. Identical text is the single case it treats as "no conflict".

Why that fails on `sample.py`:

1. Grouping by `document_id` means only chunks of one document are compared. After
   `retain_latest_policy_version`, every document in `sample.py` has exactly one chunk, so the
   inner `j` loop (`range(i + 1, 1)`) is empty, `!=` is never evaluated, and the function
   returns `[]`. The log confirms it: `inside i` prints 11 times (one per document) and
   `inside j` never prints.
2. The real contradictions in `sample.py` sit in different documents and are never compared:
   - POL005 C7 vs POL006 C8: "Cash withdrawals abroad are allowed" vs "are not allowed"
   - POL007 C9 vs POL008 C10: "Card payments are always approved" vs "above 2000 require verification"
   - POL011 C14 vs POL012 C15: "Crypto purchases are prohibited" vs "are permitted with KYC"
3. When it does fire (same document, several chunks), it over-flags: any two differently worded
   chunks count, even if they do not contradict.

Result: `retrieve_evidence` prints "No conflicting policy evidence detected." on `sample.py`, and
two unit tests fail (`test_conflict_between_different_policies_is_detected`,
`test_conflicts_detected_in_sample_data` in `test/solution_test.py`).

## Recommended change (only `solutions.py`)

Replace the per-document `!=` check with a pairwise contradiction check across all chunks.

1. Add a helper `_contradicts(text_a, text_b)` in `solutions.py`:
   - lowercase, strip punctuation, split into tokens
   - subject tokens = tokens minus stopwords and minus polarity words; require at least 2 shared
     subject tokens (e.g. "cash withdrawals", "card payments", "crypto purchases"). This avoids
     matching unrelated chunks that share one word like "card".
   - polarity: a small set of permissive words (`allowed`, `permitted`, `approved`, `always`) and
     restrictive words (`not`, `prohibited`, `require`, `requires`, `required`). Contradiction =
     one text permissive and the other restrictive, or a "not" present in only one text.
2. In `detect_conflicts`, drop the `document_id` grouping and loop over all chunk pairs `i < j`,
   appending a conflict dict when `_contradicts(...)` is true. Keep the existing output keys
   (`document_id`, `statement_1`, `statement_2`, `source_1`, `source_2`), since the tests read
   `source_1` and `source_2`. Also remove the debug `print("inside i")` / `print("inside j")` lines.
3. Leave `main.py` unchanged. `retrieve_evidence` already switches the warning on `conflicts`.

Open choice: this is a rule-based heuristic. An LLM or NLI check would be more accurate but needs
an external call, which a live-coding exercise does not need.

## Verification

- `python3 -m unittest test.solution_test` should show 26 tests passing (2 currently fail).
- `uv run main.py` on `sample.py` should give `conflicts_detected: true`, 3 conflicts (E/F, G/H, K/L)
  and the warning "WARNING: Conflicting policy evidence detected." Top evidence stays POL010 C12,
  POL001 C2, POL004 C6.
- Check no false positives: POL001 C2 vs POL003 C4 (both restrictive) and the POL009 chargeback
  chunk (shares only "card") must not be flagged.
- Afterwards update the "Open issues" section of the doc "Evidence-Aware Retrieval: Dry Run on
  Sample Dataset" so it reflects the fix.
