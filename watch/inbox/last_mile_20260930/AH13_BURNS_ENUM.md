# AH13 — burns verdict enum (refire, landed 2026-09-30)

**Owner seat files:** `tools/burns_verdict_enum.py` · `tests/test_burns_verdict_enum.py` · this receipt.
**Law kept:** `memory/burns/LEDGER.jsonl` was NEVER rewritten. sha256 `3e9afbc2cbdb4383f2dbb2155e2928669aa5b25fc3128bcace806da1f646923f` byte-identical before and after `--apply` (asserted in code, not promised in prose; git shows the file unmodified).

## 1. Census (live, 2026-09-30T12:30Z)

`693 rows · 114 distinct verdict strings · 0 rows missing verdict`. Head of the distribution: `LANDED` 310, `steal` 200, `green` 21, `landed` 19, `built` 8, `ERRATUM` 7, `vacuous` 7 … then a long tail of 62 one-off prose paragraphs (the disease AE5 row 5 named: a free-text pseudo-enum no query can GROUP BY).

## 2. Canonical enum + counts (rows / distinct)

| canonical | rows | distinct | meaning |
|---|---:|---:|---|
| LANDED | 609 | 53 | work completed / finding banked (incl. burns idiom `steal`) |
| ERRATUM | 31 | 19 | amendment to a PRIOR row (self-correction trail) |
| OPEN | 17 | 13 | owed / hold / blocked / undecidable |
| OTHER | 14 | 14 | unknown prose, all flagged review |
| PARTIAL | 9 | 8 | some landed, some owed / clause rejected |
| REJECTED | 9 | 3 | falsifier killed it (`vacuous`, …) |
| DECLINED | 3 | 3 | ask refused on bytes |
| SUPERSEDED | 1 | 1 | already executed by a concurrent lane |

**DEVIATION FLAGGED (not silent):** the operator order listed seven canonicals (LANDED/PARTIAL/REJECTED/DECLINED/SUPERSEDED/OPEN/OTHER); this landing adds an eighth, `ERRATUM`, because 31 rows / 19 distinct strings are corrections to prior rows. Collapsing them into LANDED would inflate landing counts and erasing them into OTHER would bury the ledger's self-correction trail. Veto path: drop the ERRATUM entries from `EXACT_TABLE` + rules `prefix_erratum`/`contains_erratum` in the tool; tests pin the current shape.

## 3. Mapping mechanics (never silent reclassification)

Three tiers, first hit wins, original string always preserved verbatim:

1. **Exact table** (~45 curated keys, confidence 1.0): uppercase + whitespace-collapsed join. Judgment calls carry `review=true` with a rationale (e.g. `PILOT`→PARTIAL/review, `NO_ERRATUM`→DECLINED so the contains-rule cannot flip it, `LANDED-PARTIAL-FIT`→PARTIAL curated so the LANDED prefix rule cannot absorb it).
2. **Ordered fuzzy rules** (confidence 0.80–0.90, ALWAYS `review=true`): `prefix_landed`, `prefix_erratum`, `prefix_partial`, `prefix_owed` (prefix-only by law: "gap DISSOLVES, nothing owed" must never become OPEN), `contains_blocked`, `prefix_hold`, `prefix_confirmed`, `prefix_wired`, `contains_erratum`.
3. **Fallback** `OTHER` confidence 0.30 `review=true` — unknown prose is flagged for a human, never absorbed. "TEMPLATE LANDING ONLY, flip NOT executed" lands here, not LANDED.

Review queue: **82/114 distinct strings (89 rows) flagged `review=true`** — the audit prints the full table (`--audit`), zero reads/writes.

## 4. Surface

- `normalize(verdict)` → `{original, canonical, confidence, review, rule}` — pure, deterministic, no I/O.
- `--audit` (default posture) → prints the full census table + summary above.
- `--apply` → atomically writes ONLY `memory/burns/verdict_enum_map.json` (schema `burns.verdict_enum_map.v1`; ledger sha256 embedded). Fail-closed exit 2 on malformed JSON or ledger bytes moving mid-apply.
- **Reader join contract:** `map["census"][row["verdict"]]["enum"]`; a verdict younger than the map falls back to live `normalize()`. Readers JOIN; the ledger is never the write target.

## 5. Tests (byte-backed)

`pytest tests/test_burns_verdict_enum.py -q` → **46 passed** (2026-09-30, repo venv). Coverage: exact-map clean (incl. case/whitespace), unknown→OTHER+review with original preserved, prefix/word rule assignments incl. the negation traps, map round-trip (every census key joins back to live normalize output), summary sums reconcile to row count, `--apply` leaves a fixture ledger sha-identical, malformed-line fail-closed.

## 6. Live run receipts

- census + apply executed 2026-09-30 ~12:30Z against ledger sha `3e9afbc2cbdb…`; map regenerated `2026-09-30T12:30:39Z` (693 / 114 / same sha).
- Files new (untracked, staged for the wave commit): `tools/burns_verdict_enum.py`, `tests/test_burns_verdict_enum.py`, `memory/burns/verdict_enum_map.json`, this receipt.
- Refire note: a prior AH13 seat had landed tool+tests+map but died before filing this receipt; this seat re-ran census+apply on live bytes, re-proved the 46 tests, verified the ledger hash, and filed. Only the ERRATUM deviation (§2) needs an operator glance.
