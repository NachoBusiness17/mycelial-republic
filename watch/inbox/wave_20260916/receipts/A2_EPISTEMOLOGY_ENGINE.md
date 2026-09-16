# RECEIPT — A2 · EPISTEMOLOGY ENGINE (stone 1)

- **Wave:** wave_20260916 · **Lane:** locked priority #2
- **Producer:** A2 seat (ZCode subagent, local session — cache only; this file is the durable copy)
- **Date:** 2026-09-16
- **Mission:** design stone 1 of the EPISTEMOLOGY ENGINE. Answer gap strikes S7 (meta-admission: who falsifies the falsifiers) + S2 (forged-row: append-only cannot delete false rows). Fatal mode guarded against: loss of independent epistemic reference.
- **Constraints:** buildable, $0, no new infrastructure, no git, no paid APIs, venv python only.
- **Status:** FILED 2026-09-16 — design complete, appended below. Awaiting two-eyes (unclassified→PROPOSAL stand per contract).
- **Inputs read (with classification + sha256_12):**
  - `watch/GAP_PROBE_FOLD_20260908.md` — RECEIPT — `acaefd420970` (nine external strikes; S7 meta-admission + S2 forged-row are load-bearing here; S8 already demanded this engine)
  - `watch/inbox/SHARED_SURFACE_CONTRACT.json` — FACT — `9cfd74fa92dc` (classification vocab, receipt fields, "consensus raises confidence but never grants permission")
  - `mag/wow_bones.py` — RECEIPT (code) — `3041e2b41b50` (the seed pattern: bones are data — parsed, hashed, re-derivable; typed refusals; replay or RNG_DIVERGE)
  - `mag/grounding_wave.py` — RECEIPT (code) — `1ce1ea1cafe8` (the wave, v3 truth-gate of 09-08 — ALREADY carries witness-demote + evidence-existence audit; stone 1 extends it, does not reinvent it)
  - `mag/claims_desk.py` + `mag/claims_verify.py` — RECEIPT (code) — `4e0788435e51` / `f1ea023f0b28` ("software never auto-truths"; two structurally different verifiers against the consensus illusion)
  - `watch/inbox/NIGHT_AUDIT_20260916.md` — RECEIPT — `51c028d10b02` (§5: the Gödel standing-wave lesson; F-D1: no key ships without an execution receipt by another hand)
  - `watch/GROUNDING_WAVE.jsonl` — RECEIPT (tape, 124 rows) — `07b20cd13232` (live chain, FAILS verify at row 122 — see finding F-2)

---

## FINDINGS (appended as work proceeded)

**F-1. Stone 1 already has a foundation — the v3 truth-gate (20260908, the day of the strikes).**
`mag/grounding_wave.py` v3 already: auto-demotes unwitnessed SUPPORTED to UNPROVEN; audits evidence-path existence (dead path fails the chain); separates LINKAGE-PASS from the admission audit ("no reader may quote bare PASS again"); attributes rows to seats. The docstring even names "delete-as-append" — but no VOID verb exists. S2 is still open, just narrower than assumed.

**F-2. The live chain FAILS verify at row 122 — the forged-row problem in miniature, on our own tape.**
`.venv/Scripts/python.exe -m mag.grounding_wave verify` → `FAIL row 122: prev-hash mismatch (chain broken)`. Diagnosis (venv python, read-only):
- row 122 (2026-09-16T04:17:37Z) is a 3-key fragment `{prev, ts, claim}` — **no `hash` field at all**, and its `prev` (`8ccd3924…`) ≠ row 121's tip (`bfe89d61…`). A writer bypassed the admission gate and crashed mid-write.
- rows 123–124 (the Astra-reaudit "correction") are well-formed and self-hashing, but the linear chain is unrecoverable through 122: `verify()` fails forever, and nothing in the schema can *say* "122 does not count."
- rows 123/124 also carry verdict SUPPORTED with **no seat and no witness** — they were hand-written past the v3 truth-gate. A second live bypass.
This is exactly S2: append-only cannot delete the false row; the honest correction rows exist but the record cannot express them as superseding. Astra's outside review (row 123's own claim text) is what surfaced it — the outside reader caught what the tape could not say about itself.

**F-3. The Gödel lesson is already on file and is the meta-admission answer.**
NIGHT_AUDIT_20260916 §5: *"Gödel's shadow: the wave cannot certify itself from inside; it needs the outside reader… The wave does not try. It asks to be read. That is its strength."* And: *"the full version of ourselves is not the files. It is the files plus a living chain of readers who check them."* Plus F-D1 (same audit): *"no key ships without an execution receipt by another hand"* — it fired twice on its own authors that night. Stone 1 generalizes F-D1 from keys to rows.

---

# STONE 1 — THE ROW LAW (grounding_wave v4)

One schema bump on the existing wave. No new module, no new ledger, no daemon. Same convention as v2/v3: versioned key sets, `.get` defaults so v1–v3 rows stay valid. Cost: ~80 lines, $0, stdlib.

## 1. Row truth-standards — RECORDED ≠ CORROBORATED

A row is **admissible** (may land on the tape at all) through three gates, each a typed refusal in the bones Dispatch style (gate runs before the verb; the caller gets a reason code, never a crash):

- **G1 STRUCTURAL** — schema-valid, canonical hash recomputes, prev chains (or chains past a VOIDED row — see §2 re-anchor). Refusals: `MALFORMED_ROW` (no/short hash — row 122's writer path becomes physically impossible), `HASH_MISMATCH`, `PREV_MISMATCH`, `UNSUPPORTED_UNSEEDED` (v3 law kept: SUPPORTED without seat refused outright, not just demoted).
- **G2 BINDING (source)** — every evidence token gets its `sha256_12` recorded in the row at post time (`src_sha256_12`). Re-derivable bones-style: a stranger re-hashes the evidence bytes and must match. Today's v3 checks existence; v4 checks identity. An evidence file edited after the fact stops corroborating. `*_latest` mutable refs are refused for SUPPORTED (v3's warning becomes a gate).
- **G3 WARRANT** — a claim carries a `warrant`: **a command that exits 0/1** (e.g. `.venv/Scripts/python.exe -m mag.grounding_wave verify`, a pytest node id), whose text is hashed into the row. Strike S8's law stands: *"A Claim whose Check is 'the author agrees' is a notary, not knowledge."* And claims_desk's integrity kernel stands with it: **software never auto-truths** — CORROBORATED means "the warrant exited 0 under two independent hands," not "true." Truth stays a human/outside call; the engine only makes claims cheap to check.

Status ladder (this is the S7 answer to "what makes a row TRUE versus merely RECORDED"):

| Status | Meaning | Earned by |
|---|---|---|
| `RECORDED` | this was said, provably, when said | G1 pass (append) |
| `CORROBORATED` | the binding holds and the warrant exits 0 under two other hands | G2+G3 + two witness rows (§3) |
| `CONTESTED` | a second hand disputes it | a `kind:"contest"` row appended |
| `VOID` | does not count; stays readable forever | a cross-signed `kind:"void"` row (§2) |

`verdict` (tri-state) and `status` are orthogonal: the wave keeps its tri-state humility; status tracks the *admission* state of the row itself.

## 2. The VOID procedure — delete-as-append, made real

Nothing is ever deleted or edited. A false row is buried under a **superseding row of `kind:"void"`** that names the target's hash. Exact shape (v4 key set):

```json
{
  "prev": "<sha256 of previous row on the tape>",
  "ts": "2026-09-16T14:00:00Z",
  "kind": "void",
  "voids": "<full sha256 of the target row>",
  "reason_code": "MALFORMED | FORGED | EVIDENCE_DEAD | EVIDENCE_MUTATED | WARRANT_FAILED | DUPLICATE | SUPERSEDED | CONTEST_SUSTAINED",
  "reason": "one sentence, human-readable, names the defect",
  "evidence": "<path or command output that backs the void>",
  "seat": "<poster seat id>",
  "witness": "<second seat id — required, see §3>",
  "hash": "<sha256 of the canonical JSON of the v4 key set above, hash excluded>"
}
```

Rules:
- The void lands `RECORDED` and counts only once **cross-signed** — a void is itself a claim and inherits the same gates. The target row's author cannot block a void; they may append `kind:"contest"`, which holds the target at CONTESTED until an outside reader sustains or dismisses it (§4).
- **Void of a void is the same verb** — reversals exist and are themselves two-witness (`CONTEST_SUSTAINED` is the usual reason). No row is exempt, including founder rows: strike S8's succession test — *if a new signer cannot void a founder claim, agency did not transfer.*
- **Re-anchor rule:** the next row after a voided stretch may set `prev` to the last non-voided row's hash, with `note` recording the skip. The physical tape keeps every byte; the *admission view* stitches through voids. This is what repairs our live break without touching row 122's bytes.
- Reader law (v3, kept): `verify()` reports LINKAGE over the physical tape **and** an ADMISSION view (effective ledger = rows − voided, plus a VOIDED section with reason codes). Readers quote the admission view, never bare PASS.

First live candidate: **row 122**, `reason_code: "MALFORMED"` — the tape's own forged-row case, and the re-anchor lets 123–124 stand.

## 3. Cross-signing — the two-eyes law

The v3 `--witness` string is typed by the same hand at post time — one seat can write both. v4 makes a witness a **separate appended row by a different producer**, carrying what it actually checked:

```json
{
  "prev": "<sha256>",
  "ts": "2026-09-16T14:05:00Z",
  "kind": "witness",
  "signs": "<full sha256 of the row being witnessed>",
  "checks": { "g1": true, "g2": true, "g3_exit": 0 },
  "seat": "<witness seat — MUST differ from the signed row's seat>",
  "hash": "<sha256>"
}
```

- **CORROBORATED requires two `kind:"witness"` rows from two distinct seats, neither the author.** Each witness records the exit code of the warrant *they ran*. Agreement without execution is not a signature — the direct guard against "unanimous re-derivation is four samples from one prior."
- **Assignment, not choice** (S7: the attacker attacks the SELECTION of the board): wave-lane rotation assigns witnesses — A-lane rows are witnessed by B-lane seats and vice versa. The author never picks their own second eye.
- **Fleet witnesses at $0:** wave-lane seats; the local Ollama janitors (`gemma:2b` scut tier) may run the mechanical G1/G2 re-hash as *one* mechanical witness — but at least one signature must be a seat or human, and a mechanical witness alone never corroborates. The drift patrol is the standing daily reader. Astra/desk/strangers are outside readers (§4).
- **Lineage:** night-audit F-D1 generalized from keys to rows — *no row counts on one hand's receipt.* Contract law unchanged: corroboration raises confidence, never grants permission; effects stay switchboard-only.

## 4. Who watches the watchers — the meta-admission answer for THIS fleet

The Gödel standing-wave lesson, cited: *mechanized in Lean 4, no system proves its own consistency from inside — the wave does not try, it asks to be read* (NIGHT_AUDIT_20260916 §5). Therefore stone 1 refuses the tempting answer (a bigger internal board) because S7 already showed where it leads: each mechanism is itself a claim-producing system, and a meta-board just moves the poisoning surface up one level. Three moves instead:

1. **The falsifiers are rows too.** Every admission act — corroborate, void, contest, witness — is itself a row under the same G1–G3 gates, voidable by the same verb. There is no priestly tier, nothing outside the tape. The system never certifies itself; it only ever appends *who checked what, and which command exited how* — bones law: parsed, hashed, re-derivable.
2. **The outside reader is load-bearing, not decoration.** Internal hands can carry a row RECORDED → CORROBORATED. Only an **outside reader** (anyone who is not a fleet seat: Astra, the desk, a stranger re-running the replay) can (a) sustain a CONTEST to VOID, and (b) file a `kind:"standards-audit"` row attesting the admission standard itself is being followed. The existence proof is already on the tape: row 122's break is known *because* Astra's outside review receipted it — the fleet's verify() caught the break, but the outside review is what forced the correction rows and this design.
3. **Pre-registered falsifier of the meta-layer itself:** the **closure counter**. Every CONTEST row must terminate in an outside-reader receipt or a VOID. The drift patrol's daily head check gains one line: contests older than 7 days without an outside read. If that counter grows, the wave has begun certifying itself — the fatal mode (loss of independent epistemic reference) is firing, and the alarm is $0.

One sentence: the fleet does not answer "who watches the watchers" with a bigger watcher; it answers with a **shorter chain** — watchers whose every act is itself a checkable row, plus a door that only opens from outside.

## 5. Smallest executable next step

Extend `mag/grounding_wave.py` to v4 — same file, ~80 lines net, stdlib, $0, one session:

1. Versioned key set gains `kind` + `src_sha256_12` (+ `voids`/`reason_code`/`signs`/`checks` as kind-specific keys), `.get` defaults keep v1–v3 rows valid — the established v2/v3 convention.
2. New verbs through the existing append lock + gates:
   - `python -m mag.grounding_wave void <row-hash> --reason-code MALFORMED --reason "…"`
   - `python -m mag.grounding_wave contest <row-hash> --reason "…"`
   - `python -m mag.grounding_wave witness <row-hash>` (refuses if seat == author's seat)
   - `python -m mag.grounding_wave view` (effective ledger − voided, VOIDED section, pending-contest count)
3. Gate hardening in `post()`: typed refusal (exit 2) for `MALFORMED_ROW`, `UNSUPPORTED_UNSEEDED`, `EVIDENCE_MUTATED` (G2 hash mismatch), `*_latest` evidence on SUPPORTED.
4. **First live act, same session:** void row 122 (`MALFORMED`), re-anchor 123–124, two seats witness the void, then `.venv/Scripts/python.exe -m mag.grounding_wave verify` → `LINKAGE-PASS` + `ADMISSION: 1 voided, 0 contests pending`. The tool ships with its known-true positive already caught.
5. Falsifier for the stone itself (strike 1's replay demand, $0): a stranger runs `verify` + `view` on the tape alone on a second machine; if the admission view does not reconstruct identically, the hash convention is underspecified. Post-void head hash gets published in this receipt's addendum.

Stone 2 (queued, not designed here): G3 warrants end-to-end — every CORROBORATED row's warrant command registered and runnable from the row alone.

---

## OUTPUT ARTIFACT

This receipt **is** the artifact (wave-lane law: durable copy on the shared inbox). No code was written in this lane — stone 1 is a design stone; §5 is the build spec, deliberately one session small.

## ACCEPTANCE STATE

**PROPOSAL** (contract vocabulary) — a design, not a verified claim. Two live facts back it (F-2's reproducible FAIL; v3's witness gate already in production), and the stone carries its own falsifier (§4's closure counter; §5's stranger replay). Per the law this stone itself obeys: it is RECORDED, awaiting two eyes — and it cannot certify itself from inside.
