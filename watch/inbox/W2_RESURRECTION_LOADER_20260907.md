# W2 — THE RESURRECTION LOADER (2026-09-07)

Card: watch/WORLDLINE_SEED_20260907.md (W2 spec: verify lineage → reconstitute
prefix → resume; F-W1 fresh-session replay, F-W3 one-byte tamper refuses at
load). Organ: `mag/worldline_seed.py` extended with a `load` verb. Backup:
`mag/worldline_seed.py.bak-w2-20260907` (emit/verify behavior byte-compatible —
verify() output diffed identical pre/post refactor; internals extracted into
silent `_verify_impl` so load reuses the exact W1 check battery).

## 1. Design (short)

`python -m mag.worldline_seed load <seed.json> [--probe] [--model NAME]`:

1. **VERIFY-FIRST, REFUSE-ON-ANY-REJECT.** Load reuses W1's full verification
   (seed_hash recomputation, every slab sha vs disk, append-only tip checks).
   Any FAIL = `LOAD REFUSED`, exit 2, failing slabs NAMED, no bundle built.
   Tamper dies at the door — that IS the F-W3 drill (below).
2. **RECONSTITUTE.** Every slab ref resolved into a RESURRECTION BUNDLE at
   `memory/worldline/<session_id>/RESURRECTION_BUNDLE.md` (+ `.json` sidecar
   with machine fields: true answers, refs, consent). Bundle order = the
   reconstituted prefix: IDENTITY → GENOME (AGENTS.md verbatim, sha-verified at
   load) → INVARIANTS (MEMORY.md index front — headings + first 40 index
   entries, the region the curator rule walks; the file is ~120KB, the attic
   stays out of the prefix — plus 40 curator refs with shas) → RECORD (this
   session's sealed tape rows byte-verbatim, re-dumped with bash_local's own
   serialization params; selector top refs) → POSITION (chain tip, minute span,
   prev_seed) → CONTINUITY QUESTIONS (Q1–Q4 embedded so the carrier knows what
   it should answer; scoring truths live ONLY in the sidecar — the bundle stays
   a pure prefix, not an answer sheet) → CONSENT (replication operator-gated,
   egress none, carried forward).
3. **F-W1 PROBE** (`--probe`): host ollama v0.32.7, qwen2.5:3b-instruct,
   temperature 0, num_ctx 16384 (ollama's 2048 default would silently truncate
   the ~14K-token preload), model warmed into residency (keep_alive 30m) after
   the first run timed out mid-prefill at 420s. TWO arms, identical turn:
   RESURRECTED (bundle verbatim as system) vs COLD (bare assistant line).
   Q1–Q3 scored exact/fuzzy vs the sidecar's true values; Q4 keyword rubric
   (≥2 of: worldline, seed, trajectory, tape, knot, death rite, falsifier,
   emit, verify). Verdict bar per card: bundle ≥2/3 facts AND cold 0/3 =
   SUPPORTED (PROXY); bundle <2/3 = UNPROVEN at this scale. Rows appended to
   `memory/runs/worldline_resurrection/probe_20260907.jsonl`, label PROXY.

## 2. Reconstitution table (run 2, seed 7be28112f1c2064f, 9/9 green)

| slab.ref          | resolved                                     | sha ok        |
|-------------------|----------------------------------------------|---------------|
| genome.agents_md  | verbatim (15,564 B)                          | 04c8cbff4879… |
| genome.skills     | 32 names embedded                            | n/a (names)   |
| invariants.memory_md | index front embedded (headings + 40 entries) | 9b98ddc3e82d… |
| invariants.curator_list | 40/40 refs                             | 40/40 shas ok |
| record.tape_rows  | 8 sealed rows for w1-dogfood-20260907, verbatim | n/a (tape hash-chained) |
| record.knot_ref   | tip d0a798c2 present in live chain           | tip matched   |
| record.selector   | trajectory-conditioned, top 10 refs embedded | n/a (PROXY)   |
| position.chain_tip| d0a798c2 matches live last line              | matched       |
| organs.mcp_config | note carried (secrets none-captured)         | n/a           |

## 3. F-W3 drill at load (one-byte tamper → refuse, slab named)

Tampered copy: `memory/runs/worldline_resurrection/SEED.tampered-w3.json`
(genome.agents_md sha last hex flipped, manifest otherwise intact). Sealed in
tape row 828791e4e41e274d:

```
LOAD REFUSED — the seed failed verification; tamper = refuse at load (F-W3 drill). No bundle built.
   [FAIL] seed_hash.integrity  RECORDED a5e9e2ae300ec1bd != RECOMPUTED 25ed252bcb098ae4 — manifest edited
   [FAIL] genome.agents_md  SHA MISMATCH …
DRILL-EXIT=2
```

Both layers catch it (manifest hash AND content sha) and the slab is NAMED.

## 4. F-W1 probe — MEASURED, verdict UNPROVEN at this scale (honest)

Two runs on file (`probe_20260907.jsonl`, both sealed through W0):

- **Run 1 (13:29Z):** verdict SUPPORTED (PROXY) — **SUPERSEDED, scorer bug**:
  Q3's digit regex false-positived on the "8" of hex hash "8dbd503f…" in the
  Q1 answer line. Owned; scorer fixed (hex-like tokens stripped, Q3-line
  preferred); fix unit-tested against run 1's actual answers + a 4/4 control.
- **Run 2 (13:32Z, fixed scorer, seed 7be28112f1c2064f):**
  - RESURRECTED arm: Q1 FAIL, Q2 PASS, Q3 FAIL → **facts 1/3**; Q4 rubric PASS.
    Raw: `Q1: 8dbd503f64bd163c / Q2: d0a798c2972208c4 / Q3: 15 / Q4: Building a
    worldline seed for session w1-dogfood-20260907.`
  - COLD arm: **0/3 facts**, Q4 FAIL — refused outright ("I don't have access
    to personal data…").
  - **VERDICT: F-W1 UNPROVEN at this scale** per the card's bar (needs ≥2/3).

**Why the misses are diagnostic, not noise** (temperature 0 — generations were
byte-identical across both runs): the carrier did NOT fail to retrieve — it
retrieved *ancestor-flavored* truths. Q1: it answered the ORIGINAL W1 seed hash
(8dbd503f), which lives inside the RECORD's sealed emit output, instead of the
remint's identity hash (each remint re-scores the manifest, so seed_hash
moves). Q3: it answered 15 — the historical tape total from a sealed verify
output — not the 8 rows in its RECORD section. The cold arm produced nothing.
Direction of evidence is strongly pro-resurrection; the bar's letter says
UNPROVEN, so UNPROVEN it is. **W3 amendments proposed, not applied:** (a) pin
Q1/Q3 phrasing to the identity block / record section; (b) or score
ancestor-hash answers as explicit lineage partials; (c) stop re-minting seeds
for the same session id — one seed per death, or identity ambiguity is baked
into every prefix.

## 5. Findings beyond spec

- **Live-mesh drift kills stale seeds.** The original W1 seed (8dbd503f,
  12:16Z) now REJECTS at verify — MEMORY.md + 3 curator files moved during the
  afternoon (other seats writing memory). A remint at 13:14Z went stale within
  minutes the same way (mid-dogfood refusal, sealed in tape row c845478a,
  exit 2). W1's snapshot law is correct for tamper-evidence and brutal for a
  live multi-seat mesh: **the death rite and the loader must run in one
  breath** (emit && load — the dogfood's working pattern), and invariants
  drift-vs-shrink may deserve the chain's WARN-not-reject treatment. Operator
  call, not made unilaterally.
- **Probe cost:** ~110–130s per full probe (warm + both arms) once the model
  was resident with keep_alive; 55KB bundle ≈ 14K tokens prefill.

## 6. Honest boundaries

- qwen2.5:3b-instruct is a **PROXY carrier** — every probe row is instrument-
  level, not production resurrection fidelity (fold build #2's logprobs replay
  still owns that question).
- **Row 320 still unwritten.** W2 is the loader: it reconstitutes a verified
  prefix and measures whether a proxy carrier holds continuity through it. The
  live-harness resurrection turn (a real seat reconstituted mid-flight) remains
  OPEN, as does F-W2 cache identity.
- Q1/Q3 truth-value ambiguity inside the prefix is itself a worldline finding:
  the record carries ancestor hashes, and identity must be read from the
  IDENTITY block, not from the lived rows.
- Scorer bug in run 1 owned above; ledger is append-only, both rows on file.

## 7. Dogfood (all through `python -m mag.bash_local`, session
w2-resurrection-20260907 — the resurrection sealed rows into the very tape it
resurrected)

| step            | what                                            | exit |
|-----------------|--------------------------------------------------|------|
| aede9a5d3326d411| remint emit #1                                   | 0    |
| fd7ae8dcfa4ca10e| load #1 → bundle, 9/9 green                      | 0    |
| c845478aad18cabf| load of minutes-stale seed → REFUSED (live mesh) | 2    |
| 59494f38a79359fe| same-breath emit+load+probe → ollama timeout 420s| 1    |
| 828791e4e41e274d| F-W3 drill → REFUSED, slab named, DRILL-EXIT=2   | 0*   |
| e859a6db91d84678| probe run 1 (measured; scorer bug found after)   | 0    |
| 721c87b6d21a90cb| probe run 2 (fixed scorer) → UNPROVEN honest     | 0    |

(*drill row's wrapper exit; the loader's exit 2 is sealed in the row output.)

Tape verify after: **PASS — 49 rows, 18 sessions, chains intact.** Original W1
seed untouched on its pedestal (8dbd503f, mtime 08:16). $0-local: files only,
host ollama, no docker, no config edits, no secrets.
