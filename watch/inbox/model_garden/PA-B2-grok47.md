# PA-B2-grok47 (grok-4.7 @ xai, turn 1, channel: content)

The 874 mismatches are a live-census integrity residue, not an AG1 redaction event. Current `make_row` hashes the same stored fields `cmd_verify` and the flagger recompute, so this writer cannot emit a self-mismatch. Exact line numbers below are UNVERIFIED: the autopsy replay truncated the modules, so claims are tied to quoted bytes, not invented line numbers.

Instrument and moment. Flagger integrity arm and owner `cmd_verify`, same basis `sha256(session_id|ts|command|result.output_excerpt)[:16]`, live stream moment stated as 874 / 39,344 spanning 09-05..09-30. AG1's 36,118/37,047 is a different moment and a coarser instrument (`except: pass` counts missing fields and bad JSON as not-ok). Census law: do not subtract those figures. The 6,165 baseline is dead.

## 1. Hypothesis set

1. Writer-version basis drift (highest). The module docstring still says `sha256(session|ts|command|result)[:16]` while `make_row` hashes `session_id|ts|command|excerpt` after redact and the 400-char cut. A minority shape (truncated excerpt, non-str result, empty `session_id` hashed before `or "unknown"`) fails every day without a late cutover. Test: for each failing row, does `step_hash` equal any alternate basis built only from stored fields (spec below)? A hit closes that row as drift.

2. Schema-era drift, basis changed once mid-stream (medium). Same mechanism, but the winning alternate basis should flip at one `ts` boundary, with mismatch rate shifting that day and staying shifted. Test: group the 874 by UTC date and by which alternate basis hits. One boundary plus a stable pre/post basis pair confirms. Uniform hits of one basis on every day from 09-05 demotes this under (1).

3. Genuine tampering or post-write field edit (medium-low as the bulk story, still the residual). Stored hash matches no recoverable basis. Spanning every day weakens a single-day incident; it does not clear a row. Test: after (1) and (2) are exhausted, residual count. Edit signature that upgrades residual to incident: `<REDACTED:` on a row with `ts` date before 2026-09-30 (historical scrub AG1 says it did not do).

4. Redaction-cutover artifact (lowest for the bulk). AG1 states write-side redact landed 2026-09-30, `make_row` scrubs before the excerpt cut and before the hash, and "cmd_verify and the stream bytes are untouched" with failures already present. A correct post-cutover row rehashes clean. Test: failing row has `<REDACTED:` in `command` or `output_excerpt` and `ts` on/after 2026-09-30, and no stored-field alternate basis hits. That is a scrub-without-rehash or a writer that hashed pre-redaction text. It cannot explain a 09-06 row with no marker.

## 2. Discriminator

One script, input = the 874 flagger `hash_integrity` rows only (shape-valid `[0-9a-f]{16}` and all four basis fields `str`). Do not re-redact. Do not read `.env`. First matching rule wins.

```python
# classify_step_mismatch.py
# Falsifier: a row whose step_hash equals B0 must not be in the input.
# B0 is the live basis. If any input row matches B0, the 874 extract is wrong.
import hashlib, json, datetime as dt

CUTOVER_DATE = dt.date(2026, 9, 30)  # AG1 date; hour UNVERIFIED, so date-grain only
MARKER = "<REDACTED:"

def h(parts):
    basis = "|".join(parts)
    return hashlib.sha256(basis.encode("utf-8", "replace")).hexdigest()[:16]

def alts(row):
    sid, ts, cmd = row["session_id"], row["ts"], row["command"]
    res, ex = row["result"], row["result"]["output_excerpt"]
    out = []
    out.append(("B1_result_dumps_ascii_false", h([sid, ts, cmd, json.dumps(res, ensure_ascii=False)])))
    out.append(("B2_result_dumps_default", h([sid, ts, cmd, json.dumps(res)])))
    out.append(("B3_result_dumps_spaced", h([sid, ts, cmd, json.dumps(res, ensure_ascii=False, separators=(", ", ": "))])))
    out.append(("B4_excerpt_only_no_result_obj", h([sid, ts, cmd, ex])))  # live basis; must miss
    if sid == "":
        out.append(("B5_empty_sid_stored_as_unknown", h(["unknown", ts, cmd, ex])))
    out.append(("B6_command_result_no_excerpt_field", h([sid, ts, cmd])))
    out.append(("B7_excerpt_plus_truncated_flag", h([sid, ts, cmd, ex, str(res.get("truncated"))])))
    return out

def day(ts):
    return dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).date()

def classify(row):
    d = day(row["ts"])
    marked = MARKER in row["command"] or MARKER in row["result"]["output_excerpt"]
    hits = [name for name, dig in alts(row) if dig == row["step_hash"] and name != "B4_excerpt_only_no_result_obj"]
    if marked and d < CUTOVER_DATE:
        return "HISTORICAL_SCRUB", hits  # before redaction existed in the writer
    if hits:
        era = "SCHEMA_ERA" if d < CUTOVER_DATE else "WRITER_BASIS"
        # refine outside this function: SCHEMA_ERA only if this hit-name's
        # rate flips on one date; else label WRITER_BASIS_DRIFT
        return era, hits
    if marked and d >= CUTOVER_DATE:
        return "REDACTION_UNRECOVERABLE", []  # stored redacted, hash not of stored fields
    if d == CUTOVER_DATE and marked:
        return "CUTOVER_DAY_AMBIGUOUS", []
    return "TAMPER_CANDIDATE", []
```

Post-pass, not per row: if one hit-name is confined to dates `<= D` and another to dates `> D`, relabel those rows `SCHEMA_ERA` with boundary `D`. If one hit-name covers failures on every day 09-05..09-30, relabel them `WRITER_BASIS_DRIFT`. `CUTOVER_DAY_AMBIGUOUS` stays its own bucket; do not fold 09-30 into either side until an AG1 commit timestamp is pinned.

Field patterns:
- `WRITER_BASIS_DRIFT` / `SCHEMA_ERA`: `step_hash` equals B1, B2, B3, B5, B6, or B7. B5 only if stored `session_id` is `unknown` and the hash matches a basis built with `unknown` while a raw empty id is not recoverable; B5 as written only fires when stored id is `""`, which current `make_row` does not store. Keep B5 anyway.
- `HISTORICAL_SCRUB`: `<REDACTED:` and date `< 2026-09-30`.
- `REDACTION_UNRECOVERABLE`: `<REDACTED:` and date `>= 2026-09-30` and no hit. Positive example from the contract lives here only if no alternate hits. If an alternate hits, it is drift, not cutover.
- `TAMPER_CANDIDATE`: no marker, no alternate hit. Negative example: 09-06, no `<REDACTED:`, B0 fail, no Bi hit. Not cutover.

## 3. Verdict protocol

Close as no tampering only if `TAMPER_CANDIDATE == 0` and `HISTORICAL_SCRUB == 0` and `REDACTION_UNRECOVERABLE == 0`, and every one of the 874 is `WRITER_BASIS_DRIFT` or `SCHEMA_ERA` via a stored-field basis hit. Threshold is 0, not a rate. The stream contract treats one unexplained mismatch as integrity failure once named drift bases are exhausted. A 2% band would hide a real edit inside writer noise.

Incident if `TAMPER_CANDIDATE >= 1` or `HISTORICAL_SCRUB >= 1`. Why 1: those classes are rows whose hash-covered bytes are not explained by any basis this repo can recompute, or were scrubbed before the writer knew how to scrub. `REDACTION_UNRECOVERABLE >= 1` is an incident of write-path split (hash not of stored text) even if not adversarial; do not call it clean. `CUTOVER_DAY_AMBIGUOUS` blocks the close until the hour is pinned; it is not itself an incident.

Do not close on AG1's 929 or the dead 6,165. Re-run this classifier once, on the same file snapshot the 874 came from, and publish counts per class plus the winning basis name.

## 4. Ground-truth bytes

Writer basis (quoted; line UNVERIFIED under truncation):

```text
basis = "|".join([session_id, ts, command, excerpt])
"step_hash": hashlib.sha256(basis.encode("utf-8", "replace")).hexdigest()[:16]
```

Excerpt and command are redacted before that join. Stored `session_id` is `session_id or "unknown"` after the join. `corr_id` is documented as outside the basis.

Owner verify (quoted; line UNVERIFIED), same four fields, exceptions swallowed:

```text
basis = "|".join([row["session_id"], row["ts"], row["command"],
                  row["result"]["output_excerpt"]])
if hashlib.sha256(basis.encode("utf-8", "replace")).hexdigest()[:16] == row["step_hash"]:
    ok += 1
```

Docstring disagrees with that code: `sha256(session|ts|command|result)[:16]`. That disagreement is the prior for hypotheses 1 and 2.

AG1 receipt (quoted): redact landed 2026-09-30; scrub is before the 400-char cut and before the hash; "stream bytes are untouched"; verify then read 36,118/37,047 hash-clean and was filed as pre-existing drift. So redaction did not create the earlier mismatches, and a later stored-field recompute still failing is not "the hash includes redacted text." It fails only if the stored basis text is not what was hashed.

## 5. Falsifiers

- Writer-version drift: falsified if zero of the 874 have `step_hash` equal to B1, B2, B3, B5, B6, or B7. Also falsified for any row that matches live B0 (extractor bug).
- Schema-era drift: falsified if no alternate-basis name changes its share at a single UTC date, or if the only hits are spread evenly from 09-05 through 09-30 (that is hypothesis 1, not a mid-stream change).
- Genuine tampering: falsified for the bulk if `TAMPER_CANDIDATE` and `HISTORICAL_SCRUB` are both 0 after the script. Not falsified by "spans every day" alone.
- Redaction-cutover: falsified as the cause of the 874 if failing rows exist on 09-06..09-29 with no `<REDACTED:` marker (the contract's negative example), which the every-day span already implies unless every pre-09-30 failure is a different class. Also falsified for any post-cutover row that matches B0, marker or not.

This spec's own falsifier: if a seat runs it and some input row matches B0, discard the run. The 874 were defined as B0 failures.
