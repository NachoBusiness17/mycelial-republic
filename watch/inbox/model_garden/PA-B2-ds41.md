# PA-B2-ds41 (deepseek-chat @ deepseek, turn 1, channel: content)

# 1. HYPOTHESIS SET (ranked by likelihood)

Ranking basis: the writer's hash basis is fixed in code (`mag/trajectory_step.py` `make_row`, basis = `session_id|ts|command|excerpt`); the only committed write-side change to that pipeline in the evidence window is AG1 redaction (2026-09-30). Anything that fails **before** 09-30 cannot be explained by redaction.

**H1 (very likely, dominant): Redaction-cutover basis change / partial-cutover artifact.**
- Instrument: `mag.trajectory_step.py` `make_row` at the `redact()` call and at the `basis = "|".join(...)` line; `redact()` and `redactions()` in the same file. Receipt: `watch/inbox/model_garden/premium_autopsy/evidence/B2/02__AG1_SECRETS_CONTAINMENT.md` row 3.
- Moment: 2026-09-30 (AG1 lands). Context: redaction runs BEFORE the excerpt cut AND BEFORE the hash basis, so any row whose raw `result.output_excerpt` contained a live `.env` VALUE was written with `<REDACTED:name>` in the excerpt and hashed over the redacted excerpt.
- What fails: rows written on/after 09-30 whose ORIGINAL text contained a live value (mismatch is expected and benign), plus any row on 09-30 whose basis differed for reasons below (H1b).
- **H1b (sub-hypothesis, likely): redaction cache staleness / cache-fill divergence.** `_REDACTION_CACHE` is keyed by `str(env_path)` only, not by `.env` mtime. If `.env` was edited mid-day on 09-30 (key rotation attempt, comment edits), early rows on 09-30 redact against the pre-edit value set and later rows against the post-edit set; both are "correct" under their moment, both fail re-hash against today's `.env`. This alone can explain 09-30-only failures WITHOUT any redaction marker when the rotated value is short (<`MIN_SECRET_LEN=8`) in one epoch and long in the other.

**H2 (unlikely): Writer-version drift (schema/tool version mismatch between writers).**
- Since `corr_id` was introduced (AH14) deliberately OUTSIDE the basis, corr_id drift cannot cause mismatch. But if any alternate writer (test harness, backfill script, replay tool) wrote rows to the same stream with a different basis construction (e.g., using `result.output_excerpt` of a dict-stringified `result`, or a different `EXCERPT_LIMIT=400` cutoff), those rows fail verify while looking shape-valid.
- Discriminator pattern: failures cluster by `command` prefix or by `session_id` (test sessions, one-off scripts) rather than by date.

**H3 (least likely, but the incident one): Genuine tampering of stored bytes.**
- Would require byte edits to `command`, `ts`, `session_id`, or `result.output_excerpt` after write. Evidence against per the file's own scope note: the writer enforces `schema_version` at append (`append_row` raises `SCHEMA REJECT`), and the stream is append-only by contract. A tamper hypothesis must explain WHY an attacker would edit bytes in a way that produces a uniformly 2.22% failure rate spread across 26 days.

**H4 (explicitly rejected by evidence unless H3 also holds): Pure schema-era drift mid-stream.** The trajectory_step.v1 schema is uniform across the evidence window; the only in-scope schema-adjacent change is `corr_id` (AH14), which is provably outside the basis (`mag/trajectory_step.py` comment block at AH14 correlation law: "corr_id is NOT part of the step_hash basis"). H4 is therefore not an independent hypothesis; it collapses into H2.

# 2. THE DISCRIMINATOR (one script, `classify_failing_rows.py`)

Input: paths to `steps.jsonl`, `.env`, optional `--cutover 2026-09-30`. Output: per-failing-row `{lineno, class}` with the class taxonomy below. Rules apply in order; first match wins.

Let `row` be the parsed JSON, `ts_day = row["ts"][:10]`, `excerpt = row["result"]["output_excerpt"]`, `cmd = row["command"]`.

**Class R1 - REDACTION_MARKER_IN_EXCERPT**: `"<REDACTED:" in excerpt` OR `"<REDACTED:" in cmd`.
- Interpretation: row was written by the redaction era AND at least one live value was present at write time. Mismatch against today's `.env` re-hash is EXPECTED (either the value rotated, or the row's redacted excerpt hashes differently than any pre-redaction replay). Benign.
- Positive example (from contract): row failing ONLY after 2026-09-30 with `<REDACTED:` in excerpt → R1.

**Class R2 - CUTOVER_AFTER_NO_MARKER**: `ts_day >= "2026-09-30"` AND `"<REDACTED:" not in excerpt` AND `"<REDACTED:" not in cmd`.
- Additional discriminator: run `redactions(.env)` from the current module; if ANY live value is a substring of the excerpt (case-sensitive), the row was written post-cutover WITHOUT redacting that value → this is **cache staleness** (H1b), not tampering.
- If no live value is a substring of the excerpt, this is a **post-cutover basis-basis divergence**: re-run `make_row(session_id, cmd_head, {"exit": row["result"]["exit"], "output_excerpt_raw": <the unredacted original>}, exit_code)` under the CURRENT module and see if the resulting hash matches. Match → benign write-then-edits to non-basis fields only; the excerpt bytes themselves were re-derived. No match at any plausible original → escalate to H3 inspection.

**Class R3 - PRE_CUTOVER_FAIL**: `ts_day < "2026-09-30"`.
- This is the contract's negative example: a row failing from 09-06 with no redaction marker is NOT explained by the cutover.
- Sub-classify by `session_id` and `command` pattern:
  - R3a `session_id` in a known non-`hook` namespace (e.g., test sessions, replay harnesses named in the repo, or anything not matching the writer's `event.get("session_id") or "unknown"` shape) → **H2 writer-version drift**; the row was written by a tool that reimplemented `make_row` with a different basis.
  - R3b `schema_version != "trajectory_step.v1"` → drift (should be impossible per `append_row`; presence is itself a finding).
  - R3c `command` after redaction differs from the stored `command` (i.e., `redact(row["command"], .env) != row["command"]`) for a pre-cutover row → the row was written by a pre-AG1 process AND today's `.env` contains a value that WOULD have been redacted; the row's basis used the unredacted bytes, so it fails re-hash under the current module. Valid benign explanation for pre-cutover rows containing secrets the operator has since rotated *to shorter or longer values*. This is H1 applied to the historical tail (the row is not "drifted", it is "pre-redaction").
  - R3d none of the above match and stored bytes look intact under the historical writer version → **H3 candidate**: quarantine and diff against a git-history copy of the same line if available (per AG1 row 1, the file was untracked 09-30, so git history gives byte-truth for rows written before that commit).

**Class R4 - MALFORMED**: line does not parse as one JSON object, or `result` is not a dict, or a basis field is missing/not-a-str. Owned by `hash_unverifiable` in the flagger; NOT a mismatch class.

**Class R5 - CUTOVER_EDGE**: `ts_day == "2026-09-30"` AND the row's `ts` falls within ±2h of the AG1 commit moment (available from git log of `githooks/pre-commit`). Both redaction-era and pre-redaction rows can exist on this day. Treat as R1 if `<REDACTED:` present, else apply R2 logic.

The classifier emits, per failing row, one of `{R1, R2, R3a, R3b, R3c, R3d, R5, R4}` plus the specific discriminator value that fired.

# 3. VERDICT PROTOCOL

Close as **no tampering** iff, over all 874 failures:

- `count(R1) + count(R2) + count(R5) + count(R3c) >= 0.90 * 874` AND
- `count(R3d) == 0` AND
- `count(R3a) + count(R3b) <= 0.10 * 874` (writer-version drift tolerates old test-harness sessions, but a high share means a production writer is wrong; see falsifier for H2) AND
- no failing row has `ts_day < "2026-09-30"` AND `command` and `excerpt` both byte-identical to a git-history version AND `step_hash` differs from the git-history `step_hash` (that pattern IS tampering regardless of count).

Declare **incident** iff `count(R3d) >= 1` OR the last bullet fires. The threshold "0.90 / 0" is chosen because H1/H1b/H2 predictions are additive: any single unexplained pre-cutover row whose bytes are git-stable is a positive signal of tamper, and pivoting on a single row is the correct conservative move for a stream with an open secret-leak window (AG1 "Not done here" item 1: keys not yet rotated).

If `count(R2) > 0` but no live value is a substring of any R2 row: that count is itself a bug in the AG1 cache (`_REDACTION_CACHE` is unfalsified there) and must be fixed before the verdict closes; the protocol therefore requires the cache-fixer to land first.

# 4. EVIDENCE BYTES (ground truth quoted)

Hash basis, writer side, `mag/trajectory_step.py` `make_row`:
```
basis = "|".join([session_id, ts, command, excerpt])
...
"step_hash": hashlib.sha256(basis.encode("utf-8", "replace")).hexdigest()[:16],
```
Hash basis, verifier side, `mag/trajectory_step.py` `cmd_verify`:
```
basis = "|".join([row["session_id"], row["ts"], row["command"],
                  row["result"]["output_excerpt"]])
if hashlib.sha256(basis.encode("utf-8", "replace")).hexdigest()[:16] == row["step_hash"]:
```
Flagger side, `watch/inbox/.../anomaly_flagger.py` module docstring, hash_integrity paragraph:
```
recompute the basis sha256(session_id|ts|command|result.output_excerpt)[:16] -
OWNED by mag.trajectory_step make_row/verify, READ here, never rewritten
```
Containment order in `make_row`:
```
# Containment order matters: redact the FULL text BEFORE the excerpt cut (a
# value straddling the 400-char boundary would otherwise land half-live)
# and BEFORE hashing (verify recomputes over the redacted basis).
```
Cache key, `mag/trajectory_step.py`:
```
def redactions(env_path: Path | str = ENV_PATH) -> list[tuple[str, str]]:
    key = str(env_path)
    if key not in _REDACTION_CACHE:
```
corr_id exclusion, `mag/trajectory_step.py` AH14 comment block:
```
# corr_id is NOT part of the step_hash basis, so
# `verify` recomputes pre-AH14 and post-AH14 rows identically
```
Pre-existing failure count, `02__AG1_SECRETS_CONTAINMENT.md` "Evidence" section: `verify` reads `36,118/37,047` hash-clean on 2026-09-30 → `929` mismatched rows already present **before** the flagger's Q36 arm existed. The flagger now reports `874 of 39,344` on 2026-10-01. The delta between 929 (pre-Q36, on 09-30) and 874 (post-Q36, on 10-01) is not a contradiction: the two runs used different instruments (see census law in the same file, and the contract's "old 6165-row baseline did not reproduce at re-probe"). Only the 874-at-2026-10-01 count is a verdict-worthy measurement.

# 5. FALSIFIER PER HYPOTHESIS

**H1 (redaction-cutover basis change).** Falsified if any pre-cutover row (`ts_day < "2026-09-30"`) fails verification AND has no `command`/`excerpt` substring matching any live OR historical `.env` value, AND that row's bytes are git-stable. That row is not redaction-explainable.

**H1b (redaction cache staleness on 09-30).** Falsified if the classifier identifies R2 rows whose excerpt contains a CURRENT live `.env` value (i.e., the row was written post-cutover but the live value landed verbatim). If zero such rows exist and R2 count is still large, the mismatch is not cache staleness and the post-cutover basis shape diverged another way; escalate to H2.

**H2 (writer-version drift).** Falsified if every R3a/R3b row's `command` prefix and `session_id` fall inside the known non-hook namespaces already named in the repo (test fixtures, replay harnesses, backfill tools). If any R3a row's `session_id` matches a live hook session and its `command` is a production invocation, the producer of that row needs its own patch, not a classification.

**H3 (genuine tampering).** Falsified if for every R3d candidate the row's bytes match a git-history copy of the same line at the commit immediately preceding the row's `ts` (via `git log -S<step_hash>` on `memory/trajectory/steps.jsonl` before the 09-30 `git rm --cached`). Byte-stability plus hash-mismatch plus no redaction/basis explanation is the ONLY sufficient condition for H3; absent all three, tampering is not accused.

**H4 (schema-era drift).** Falsified as an independent hypothesis: every `trajectory_step.v1` row has a fixed basis shape; the only mid-window shape change (`corr_id`) is documented as outside the basis. Any row claiming "schema drift" as cause must name a schema_version other than `trajectory_step.v1`; the taxonomy folds those into R3b.

# The one landable deliverable

`watch/inbox/mountain_climb/classify_steps_mismatch.py`: reads `steps.jsonl`, `.env`, and `git log --follow` for pre-09-30 rows; applies the rule order in §2; prints a CSV `lineno,ts,step_hash,class,discriminator` plus a summary counter that feeds §3's threshold test directly.

Falsifier for the deliverable itself: on a synthetic stream where 10 rows are hand-crafted to match R1, 10 to match R2-with-live-substring, 10 to match R3c, and 1 to match R3d (byte-tampered pre-cutover row), the classifier must output exactly `{R1:10, R2:10, R3c:10, R3d:1}` and the summary must trip the §3 incident clause on the single R3d. If it does not, the rule order is wrong and the deliverable is not landed.
