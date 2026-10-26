# PA-B2-glm53 (glm-5.3-flash @ zai, turn 1, channel: content)

# TRIAGE: the 874 hash-integrity failures on memory/trajectory/steps.jsonl

**Citations note:** the evidence replay truncates all three code files without line numbers. Quotes below resolve to quoted bytes; numeric line cites are marked UNVERIFIED. One instrument, one moment: anomaly_flagger.py integrity arm, 2026-09-30 sweep, vs mag.trajectory_step cmd_verify same moment.

## Ground truth bytes (deliverable 4)

The basis, writer side (mag/trajectory_step.py, make_row, quoted):

```
text = redact(text, env_path)
excerpt, truncated = text[:EXCERPT_LIMIT], len(text) > EXCERPT_LIMIT
command = redact(command[:2000], env_path)
basis = "|".join([session_id, ts, command, excerpt])
"step_hash": hashlib.sha256(basis.encode("utf-8", "replace")).hexdigest()[:16],
```

Verify side (cmd_verify, quoted):

```
basis = "|".join([row["session_id"], row["ts"], row["command"],
                  row["result"]["output_excerpt"]])
```

Four load-bearing facts from these bytes:

- F1: redaction happens BEFORE hashing, and AG1 states this was landed "so no live value lands in the stream and `verify` stays self-consistent" (02__AG1, item 3). Post-cutover rows are redaction-coherent by construction. The contract's redaction-artifact hypothesis requires the stored basis to include redacted text the hash never saw; the writer bytes make that impossible for rows written after cutover. It is only possible for rows whose TEXT was redacted after hashing, and AG1 records "NO history rewrite" (operator decision, 02__AG1 header) - no in-place redaction pass exists.
- F2: EXCERPT_LIMIT=400 and command cap [:2000] are applied to BOTH sides only if the stored row is the truncated text - it is, so truncation is not a mismatch source at any single writer era. A mismatch source exists only if an EARLIER writer used a different cap or a different basis shape.
- F3: AG1, Evidence section: "Pre-existing (NOT caused by this change - `cmd_verify` and the stream bytes are untouched): `verify` reads 36,118/37,047 rows hash-clean." That is 929 failing rows on 09-30, before the integrity arm existed, and the failure predates the redaction commit. The 874 figure is the flagger's count on its own moment; the delta 929 vs 874 is itself a datum (55 rows moved classes between instruments - see class U below).
- F4: corr_id is "deliberately NOT in the step_hash basis" (01__trajectory_step.py, AH14 block) - so the AH14 schema-era addition cannot produce mismatches. Schema-era drift via corr_id is falsified by bytes already in evidence.

## Deliverable 1: HYPOTHESIS SET (ranked)

**H1 - Writer-version basis drift (most likely).** An earlier make_row hashed a different basis shape (different excerpt cap, no truncation, different join order, un-redacted command field, or a ts timespec change, e.g. seconds vs milliseconds precision). All rows from that writer era fail deterministically; every-day span fits because the old writer ran across the whole stream. The 09-05 stream start (01__trajectory_step.py: "The tesuji ... 09-05") and a single stream-wide failing cohort is exactly a basis-shape signature, not a tamper signature (tamper clusters, it does not carpet 26 days).

**H2 - Redaction-cutover artifacts.** Only via the one live path: rows written 09-30 whose command or excerpt contains a live .env value that redact() caught AFTER hashing in some interleaving (e.g. .env edited between hash and a manual re-append, or MAG_ENV_FILE differing between writer and a test fixture write - AG1: "MAG_ENV_FILE override exists so tests use synthetic fixtures"). Bounded expectation: rows on 09-30 only, all containing `<REDACTED:` markers or .env substrings.

**H3 - Genuine tampering (least likely on current facts).** Edited output_excerpt or command under a retained hash. The flagger's own Q36 note is the counter-instrument: shape-only checks previously let "mutated text under a shape-valid 16-hex hash read clean" (00__anomaly_flagger.py header), so mutation is possible - but carpet distribution over every day and the owner's identical verify failures point away from targeted editing.

**H4 - Basis-non-str rows (verifiability gap, not mismatch).** Rows where a basis field is not a str (excerpt is a dict/list from an old writer). The flagger routes these to hash_unverifiable; cmd_verify's bare `except: pass` silently counts them failed. These are the 55-row 929-vs-874 delta candidates.

## Deliverable 2: THE DISCRIMINATOR (classifier spec)

One script, `classify_mismatch.py`, input = the failing-row line numbers from the flagger run. For each failing row R:

```
parse R as JSON; if unparseable -> class MALFORMED (out of scope, flagger owns it).
fields: ts (first 10 chars = day), session_id, command, result.output_excerpt.

T1  if ts day != "2026-09-30" AND "<REDACTED:" in command or excerpt
        -> class UNEXPLAINED_REDACT_MARK (escalate; redact() runs pre-hash,
           a pre-hash marker means the hash input contained the marker:
           consistent, so actually -> class V_REDACT_COHERENT, informational)
T2  recompute basis A = "|".join([session_id, ts, command, excerpt])
        if sha256(A)[:16] == step_hash -> class V_CLEAN (instrument disagreement; investigate)
T3  candidate alternate bases, in order:
    B1: excerpt cut at 200, 300, 512, 1000 instead of 400
    B2: command NOT truncated (full stored command)
    B3: basis = "|".join([session_id, ts, command, result_json_canonical])
    B4: ts with timespec="seconds" (strip .mmm)
    B5: basis includes exit code: "|".join([..., str(exit), excerpt])
    B6: pre-AH14 shape: basis over row minus corr_id (should equal A; keep as guard)
    if any Bi matches -> class W_WRITER_DRIFT:<Bi>  (record Bi and the
        day-range of rows matching Bi; a clean day boundary = the cutover date)
T4  if any basis field is not a str -> class U_UNVERIFIABLE
T5  if ts day == "2026-09-30" AND ("=" + live .env value) substring present
        in command or excerpt -> class R_CUTOVER_ARTIFACT
T6  else -> class X_TAMPER_CANDIDATE
```

Positive example (per contract): row, ts 2026-09-30T14:xx, excerpt contains `<REDACTED:HERMES_API_KEY_1>`, matches no alternate basis, matches A -> V_REDACT_COHERENT, not tampering. Negative example: row, ts 2026-09-06T03:xx, no redaction marker, matches B1 (excerpt cut 200) -> W_WRITER_DRIFT:B1 with cutover day 09-06; if it matches NO basis at all -> X_TAMPER_CANDIDATE.

## Deliverable 3: VERDICT PROTOCOL

- **NO TAMPERING (drift closure):** X_TAMPER_CANDIDATE = 0 AND (W_WRITER_DRIFT + R_CUTOVER_ARTIFACT + U_UNVERIFIABLE + V_REDACT_COHERENT) = 874. Threshold zero because tampering is a per-row verdict: one unexplained row is one tamper event; a percentage threshold would launder a real incident into a rounding error. Any residual N>0 -> downgrade to INCIDENT-UNCERTAIN, not clean.
- **INCIDENT:** X_TAMPER_CANDIDATE >= 1, escalated immediately if any X rows share session_id or fall in a contiguous ts run (targeted-edit signature per the Q36 mutated-text class).
- **Additional closure gate:** re-run the flagger integrity arm once at a second named moment; X count must be identical (X rows cannot self-heal; a shrinking X means the instrument, not the stream, moves).

## Deliverable 5: FALSIFIERS

- H1 falsified if: no alternate basis Bi matches any failing row, OR the Bi-matching rows do NOT partition on a clean ts boundary (a real writer version has a single cutover day; scattered matches across eras = coincidence, not versioning).
- H2 falsified if: zero R_CUTOVER_ARTIFACT rows exist outside 09-30, or (stronger) any row failing while containing an un-redacted live .env value - that is the opposite of the cutover signature and AG1's own pre-commit gate story contradicts it.
- H3 falsified if: X_TAMPER_CANDIDATE = 0 at two named moments. H3 confirmed only by X rows whose text mutates between moments with a constant step_hash.
- H4 falsified if: the U_UNVERIFIABLE count is 0 while the 929-minus-874 delta persists (delta then needs a new owner).
- Baseline note: the 6165-row baseline's non-reproduction at re-probe is consistent with H1 only if the re-probe used a different row census moment (append-only stream: "row counts are a census of one moment, never a constant", 00__anomaly_flagger.py surface 1 note). It is NOT evidence of healing and must not be scored as such.

**Deliverable falsifier (this spec):** run classify_mismatch.py on the flagger's named row list. If the class histogram sums to less than the failing count, or any row lands in two classes, the classifier is wrong and the spec fails its own gate.
