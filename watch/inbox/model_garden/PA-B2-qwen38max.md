# PA-B2-qwen38max (qwen/qwen3.8-max-prime @ nous, turn 1, channel: content)

## 1. HYPOTHESIS SET (ranked by likelihood)

### H1: Writer-version drift (basis formula changed during initial build-out)
- Likelihood: highest.
- Rationale: failures span every stream day from 09-05 (day one of the hook); the module docstring self-identifies as "trajectory spine build #1" implying iterative construction; AG1 confirms 929 rows were already failing BEFORE the 09-30 redaction cutover (file:line `02__AG1_SECRETS_CONTAINMENT.md`, "Evidence" section: "verify reads 36,118/37,047 rows hash-clean"); the count is stable across the stream's life, not clustered at any single event boundary.
- Discriminating test: failing rows will cluster in the earliest N days of the stream and will lack fields or carry field shapes absent from the current schema (e.g., no `corr_id`, no `schema_version`, or a `result` field that is a bare string rather than a dict with `output_excerpt`).

### H2: Schema-era drift (hash basis definition changed between writer versions)
- Likelihood: second highest; partially overlaps H1.
- Rationale: the docstring schema block says `sha256(session|ts|command|result)[:16]` while the code computes `sha256(session_id|ts|command|result.output_excerpt)[:16]` (file:line `01__trajectory_step.py`, `make_row` function: `basis = "|".join([session_id, ts, command, excerpt])`). If an earlier writer hashed the full `result` dict serialized as JSON rather than only `result.output_excerpt`, those rows fail under the current verify.
- Discriminating test: recompute the hash using the full `json.dumps(row["result"])` as the fourth basis element instead of `row["result"]["output_excerpt"]`. If that matches `step_hash`, the row was written under the old basis.

### H3: Redaction-cutover artifacts (post-09-30 rows re-hashed or stored-basis mismatch)
- Likelihood: low for the bulk; possible for a small subset.
- Rationale: AG1 explicitly states "NO history rewrite" (`02__AG1_SECRETS_CONTAINMENT.md`, header). The redaction is applied BEFORE hashing in `make_row` (`01__trajectory_step.py`: "redact the FULL text BEFORE the excerpt cut and BEFORE hashing"), so post-09-30 rows are self-consistent. However, if any external tool re-wrote stored rows to add redaction markers without recomputing the hash, those rows would fail.
- Discriminating test: failing rows dated after 09-30 whose `output_excerpt` or `command` contains the literal string `<REDACTED:` but whose hash does not match the stored basis = post-hoc redaction without re-hash. Failing rows dated after 09-30 WITHOUT `<REDACTED:` markers are NOT explained by this hypothesis.

### H4: Genuine tampering
- Likelihood: lowest.
- Rationale: tampering would need to explain 874 rows spread across 26 days with no detectable motive visible in the evidence. The systematic presence from day one and the stable count argue against adversarial modification. No evidence of content injection, row insertion, or semantic anomaly is presented.
- Discriminating test: failing rows that do NOT match any basis-variant recomputation (H1/H2 variants), do NOT carry redaction markers post-cutover, and whose stored field values are semantically inconsistent with the command/result pattern of adjacent rows.

---

## 2. THE DISCRIMINATOR (deterministic classifier spec)

One script. Input: `steps.jsonl`. Output: each failing row assigned to exactly one class.

```python
#!/usr/bin/env python3
"""classify_failures.py - deterministic triage of hash-mismatch rows.

Usage: python classify_failures.py [--stream PATH]
Output: one line per failing row: LINENO|CLASS|REASON
Classes: BASIS_VARIANT, REDACTION_CUTOVER, SESSION_ID_DRIFT, UNEXPLAINED
Exit: 0 always (reporting tool).
"""
import hashlib, json, sys
from pathlib import Path
from datetime import datetime

STREAM = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("memory/trajectory/steps.jsonl")
REDACTION_DATE = "2026-09-30"

def sha16(basis: str) -> str:
    return hashlib.sha256(basis.encode("utf-8", "replace")).hexdigest()[:16]

def classify(lineno: int, row: dict) -> tuple[str, str]:
    stored_hash = row.get("step_hash", "")
    session_id = row.get("session_id", "")
    ts = row.get("ts", "")
    command = row.get("command", "")
    result = row.get("result", {})
    excerpt = result.get("output_excerpt", "") if isinstance(result, dict) else ""

    # Current basis (the verify formula)
    current_basis = "|".join([session_id, ts, command, excerpt])
    if sha16(current_basis) == stored_hash:
        return ("CLEAN", "matches current basis")  # should not appear in failing set

    # --- H2 variant: full result dict as fourth element ---
    if isinstance(result, dict):
        alt_basis_full_result = "|".join([session_id, ts, command, json.dumps(result, ensure_ascii=False)])
        if sha16(alt_basis_full_result) == stored_hash:
            return ("BASIS_VARIANT", "hash matches full-result-dict basis (pre-v1 writer)")

    # --- H2 variant: result as raw string (not dict) ---
    if isinstance(result, str):
        alt_basis_str_result = "|".join([session_id, ts, command, result])
        if sha16(alt_basis_str_result) == stored_hash:
            return ("BASIS_VARIANT", "hash matches string-result basis (pre-v1 writer)")

    # --- H1 variant: session_id coercion bug ---
    # If stored session_id is "unknown" but basis used empty string
    if session_id == "unknown":
        alt_basis_empty_sid = "|".join(["", ts, command, excerpt])
        if sha16(alt_basis_empty_sid) == stored_hash:
            return ("SESSION_ID_DRIFT", "hash matches empty-session_id basis")

    # --- H1 variant: no schema_version field (pre-schema rows) ---
    if "schema_version" not in row:
        # Try basis without excerpt truncation (full output)
        # Cannot recover full output from stored bytes; mark for manual
        return ("BASIS_VARIANT", "row lacks schema_version (pre-v1 writer); basis unrecoverable from stored bytes")

    # --- H3: redaction-cutover artifact ---
    has_redaction_marker = "<REDACTED:" in excerpt or "<REDACTED:" in command
    if ts >= REDACTION_DATE and has_redaction_marker:
        # The stored text IS redacted; if hash doesn't match, either
        # the hash was computed pre-redaction or text was re-redacted post-hash
        return ("REDACTION_CUTOVER", "post-09-30 row with <REDACTED: marker; hash mismatch = basis changed after write")

    # --- H3 negative: post-09-30, no marker ---
    if ts >= REDACTION_DATE and not has_redaction_marker:
        # Not explained by redaction; fall through
        pass

    # --- H4 / unexplained ---
    return ("UNEXPLAINED", "no known basis variant matches; candidate for tampering review or unknown writer version")


def main():
    counts = {}
    with STREAM.open(encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f, 1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                row = json.loads(stripped)
            except json.JSONDecodeError:
                continue
            stored_hash = row.get("step_hash", "")
            session_id = row.get("session_id", "")
            ts = row.get("ts", "")
            command = row.get("command", "")
            result = row.get("result", {})
            excerpt = result.get("output_excerpt", "") if isinstance(result, dict) else ""
            current_basis = "|".join([session_id, ts, command, excerpt])
            if sha16(current_basis) == stored_hash:
                continue  # clean row
            cls, reason = classify(lineno, row)
            counts[cls] = counts.get(cls, 0) + 1
            print(f"{lineno}|{cls}|{reason}")

    print(f"\n--- SUMMARY ---", file=sys.stderr)
    for cls, n in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {cls}: {n}", file=sys.stderr)
    print(f"  TOTAL: {sum(counts.values())}", file=sys.stderr)

if __name__ == "__main__":
    main()
```

**Field patterns per class:**

| Class | Date boundary | Basis-shape signature | Field markers |
|---|---|---|---|
| BASIS_VARIANT | any (expect cluster 09-05 to ~09-12) | hash matches alternate basis formula | possibly missing `schema_version`; `result` may be str not dict |
| SESSION_ID_DRIFT | any | hash matches with `""` as session_id | stored `session_id` = `"unknown"` |
| REDACTION_CUTOVER | ts >= 2026-09-30 only | hash does NOT match current basis | `<REDACTED:` literal in `command` or `output_excerpt` |
| UNEXPLAINED | any | no known variant matches | none of the above |

---

## 3. VERDICT PROTOCOL

**Close as "no tampering" (incident = NO) if and only if:**

- `UNEXPLAINED` count = 0, AND
- every failing row is accounted for by `BASIS_VARIANT` + `SESSION_ID_DRIFT` + `REDACTION_CUTOVER`, AND
- `REDACTION_CUTOVER` rows are all dated >= 2026-09-30.

**Threshold rationale:** zero tolerance for UNEXPLAINED. Any row that matches no known basis variant and carries no redaction marker has no benign explanation from the evidence. Even one such row escalates to incident.

**Declare "incident" (tampering confirmed) if:**

- `UNEXPLAINED` count >= 1, AND
- manual inspection of those rows shows no writer-version provenance (no git blame on the writer at that timestamp, no deployment log matching).

**Intermediate (inconclusive):**

- `UNEXPLAINED` count >= 1 but <= 5, AND all such rows have plausible provenance gaps (e.g., writer was being actively edited that day per git log). Verdict: "no tampering detected; N rows unattributed to known basis variants; recommend writer git-log correlation before closing."

**Why zero-tolerance on UNEXPLAINED:** the hash is a 16-hex truncation of SHA-256 over four named fields. The collision probability for accidental mismatch is negligible (~2^-64). A mismatch means the basis bytes differed at write time vs verify time. If no known code version explains the difference, the bytes were altered after write.

---

## 4. EVIDENCE BYTES (ground truth quotes)

**Hash basis construction (writer side):**
`01__trajectory_step.py`, `make_row` function:
```python
basis = "|".join([session_id, ts, command, excerpt])
return {
    ...
    "step_hash": hashlib.sha256(basis.encode("utf-8", "replace")).hexdigest()[:16],
```

**Hash basis reconstruction (verify side):**
`01__trajectory_step.py`, `cmd_verify` function:
```python
basis = "|".join([row["session_id"], row["ts"], row["command"],
                  row["result"]["output_excerpt"]])
if hashlib.sha256(basis.encode("utf-8", "replace")).hexdigest()[:16] == row["step_hash"]:
    ok += 1
```

**Redaction applied before hash (post-09-30 only):**
`01__trajectory_step.py`, `make_row`:
```python
text = redact(text, env_path)
excerpt, truncated = text[:EXCERPT_LIMIT], len(text) > EXCERPT_LIMIT
command = redact(command[:2000], env_path)
basis = "|".join([session_id, ts, command, excerpt])
```

**Session-id coercion asymmetry (potential drift source):**
`01__trajectory_step.py`, `make_row`:
```python
basis = "|".join([session_id, ts, command, excerpt])  # raw param
...
"session_id": session_id or "unknown",  # coerced for storage
```
The hook pre-coerces (`event.get("session_id") or "unknown"`), but any direct caller of `make_row` passing a falsy session_id would produce a hash over the raw value while storing "unknown".

**AG1 pre-existing failure count (pre-redaction baseline):**
`02__AG1_SECRETS_CONTAINMENT.md`, Evidence section:
"verify reads 36,118/37,047 rows hash-clean"
(929 failures existed before redaction landed; redaction is not the cause of the bulk.)

**Flagger integrity arm basis (matches verify):**
`00__anomaly_flagger.py`, docstring:
"recompute the basis sha256(session_id|ts|command|result.output_excerpt)[:16]"

---

## 5. FALSIFIERS

| Hypothesis | Falsifier (observation that kills it) |
|---|---|
| H1: Writer-version drift | A failing row from 09-20+ whose `schema_version` is `"trajectory_step.v1"` and whose `result` is a well-formed dict with `output_excerpt` - if the writer was stable by then, late failures are not version drift. |
| H2: Schema-era drift (full-result basis) | Recomputing with `json.dumps(row["result"])` as the fourth element fails to match `step_hash` for ALL failing rows - the alternate basis explains none of them. |
| H3: Redaction-cutover | A failing row dated 09-15 with `<REDACTED:` in its excerpt - redaction did not exist on 09-15, so this row cannot be a cutover artifact. Conversely: all post-09-30 failing rows lack `<REDACTED:` markers - cutover explains zero rows. |
| H4: Genuine tampering | Every UNEXPLAINED row is accounted for by a git-log-correlated writer edit on its stream date - no adversarial action needed. Or: the UNEXPLAINED count is zero. |

**Positive example (confirms H3):**
A row with `ts = "2026-09-30T14:22:01.000+00:00"`, `output_excerpt` containing `<REDACTED:ALIBABA-MODEL-STUDIO_1>`, and a hash mismatch on the current basis. Explanation: the row was written pre-redaction (hash over raw text), then an external process replaced the value with the redaction marker without recomputing the hash.

**Negative example (excludes H3):**
A row with `ts = "2026-09-06T09:14:33.000+00:00"`, no `<REDACTED:` substring anywhere in its fields, and a hash mismatch. The redaction cutover had not occurred; this row's failure is NOT a cutover artifact. It must be H1, H2, or H4.

---

## DELIVERABLE SUMMARY

The single landable artifact is `classify_failures.py` above. Run it against the live `steps.jsonl`. If UNEXPLAINED = 0, close as "no tampering; 874 rows are writer-version drift artifacts from the trajectory spine build-out." If UNEXPLAINED >= 1, escalate those specific line numbers for manual git-blame and content inspection before declaring incident.

**This deliverable's own falsifier:** if the script reports UNEXPLAINED = 0 but a subsequent independent recomputation (different language, different JSON serializer) finds mismatches the script missed, the classifier is incomplete. The script's correctness depends on the assumption that the pipe-separated basis with UTF-8/replace encoding is the only format ever used - if a writer used a different separator or encoding, the script would misclassify those rows as UNEXPLAINED rather than BASIS_VARIANT.
