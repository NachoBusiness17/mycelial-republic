# A3_corroboration_bootstrap (anthropic/claude-opus-5.5, turn 1)

# RIB DRAFT: Lineage-Distinct Corroboration (bootstrap of the 0-corroborated ladder)

## Conditions and citation register

**Read before relying on any number below.** I ran no commands and read no source bytes in this sitting. Every code claim is carried from the two receipts in evidence.

- A row is marked **RQ** when the receipt quotes the bytes.
- A row is marked **UNVERIFIED** when the receipt paraphrases.
- The applying seat must re-read each cited line range before landing the patch in section 4.

| ID | Location | Bytes as carried by receipt | Status |
|---|---|---|---|
| C1 | mag/grounding_wave.py:325-335 | CORROBORATED requires `len(seats) >= 2`, distinct seats, neither the author, all checks passing | RQ for `len(seats) >= 2`; the surrounding logic is UNVERIFIED |
| C2 | mag/grounding_wave.py:552, :519 | `"seat": str(seat).strip()`, default `"zcode"` | RQ |
| C3 | mag/grounding_wave.py:642-646 | SELF_SIGNED refusal when witness seat == author | UNVERIFIED (paraphrase) |
| C4 | mag/grounding_wave.py:647-655 | `witness()` executes g1/g2/g3 and records `checks = {g1, g2, g3_exit}` | RQ for the dict shape; execution is UNVERIFIED |
| C5 | mag/grounding_wave.py:217-231, :702-722 | G2 `_bind_sources`, re-hashed at verify by `_evidence_mutated` | UNVERIFIED |
| C6 | mag/grounding_wave.py:472-482 | G3 `_run_warrant` | UNVERIFIED |
| C7 | mag/grounding_wave.py:130-131 | `VOID_REASONS` enum includes FORGED (SUPERSEDED observed on row 134) | UNVERIFIED |

**Measurement M1 (the baseline this rib moves):**

- **Instrument:** `.venv\Scripts\python.exe -m mag.grounding_wave verify` plus a json census of `watch/GROUNDING_WAVE.jsonl`.
- **Moment:** the w4-06 session. It is no earlier than 2026-09-27T18:39:49Z, since the census includes the batch ending then. The exact run time is not recorded.
- **Context:** read-only, venv python, Windows.
- **Result:** 137 rows, 5 witness rows, all with seat=operator; `ADMISSION: ... 0 corroborated`; 0 rows carry `src_sha256_12`; 0 rows carry `warrant`.
- **Staleness:** the ledger may have moved since. Re-run M1 before step 1 of section 2.

**A load-bearing observation from C1+C2.** The current rule counts distinct seat *strings*, and the seat is an unauthenticated free string. Operator plus any second string already satisfies `len(seats) >= 2` today. So the 0 is a volunteering outcome, not a hard lock, and the first row that "unlocks" it under the current rule could be a puppet. That is why section 4 lands before section 2 produces its row.

---

## (1) Witness taxonomy

### Definition

<rule>
Corroboration exists to catch errors the author cannot see. Two parties are DISTINCT for corroboration iff their errors on the claim are plausibly uncorrelated.

Operationally, witness W is distinct from party X iff both of the following hold:

- **F1, reasoning-substrate lineage.** W and X have different lineages. A lineage is a model family by vendor/weights origin, or `human`. Fine-tunes, quantizations, prompts, keys, and seat names do not create a new lineage.
- **F3, context-blind.** W judged from the witness packet only (claim bytes, evidence paths, evidence hashes, warrant). W did not see X's transcript, reasoning, or verdict.

A CORROBORATED claim needs two witnesses that are pairwise distinct from each other AND each distinct from the author.
</rule>

### Axes considered and their status

| Axis | Status | Why |
|---|---|---|
| Separate key material | **Necessary for attribution, not sufficient for distinctness** | One operator issues every key (the mates' auth whitelist, the xAI key, MCP credentials). Two keys held by one controller over one lineage give one opinion twice. |
| F1 lineage | **Required** | Same-lineage seats share training-induced blind spots. Their agreement is closer to recomputation than to independent observation. |
| F2 execution substrate (host + interpreter running g1/g2/g3) | **Recorded, not required in v1** | Only one box exists, so requiring F2 makes the rung unreachable again. The residual risk is bounded because g2/g3 are recomputable by any later reader (C4, C5). A poisoned venv yields the same check results for every local witness. |
| F3 context-blind | **Required** | A witness fed the author's reasoning is an echo, whatever its lineage. |
| Separate economic interest | **Out of reach; declared, not faked** | Every seat answers to one residual claimant (w4-trust-game s3(b), Holmström). Under this rib, CORROBORATED means "independently checked by two disjoint reasoning substrates under one owner". It does NOT mean "independently interested". Only the stranger test can supply this axis. |

### Example pairs

**Pair A (the contract's case)**
- NEG: a local mate on the box witnesses its own output under the seat string `mate3-review`. F1 is identical to the author because it *is* the author, and F3 is violated because it holds its own reasoning. C3 catches this only if the strings match exactly. Under C2 a renamed string passes C3, which is exactly the hole this rib closes.
- POS: a local mate whose lineage differs from the author's witnesses a `<L>/zcode` claim, receiving only the packet. F1 differs and F3 holds. F2 is shared and gets recorded.

**Pair B (same family, many seats)**
- NEG: author `zcode`, witnesses `zcode-desk` and `zcode-wave-driver-v0`. These are real seat strings from the M1 census. All three are one lineage, so this counts as zero distinct witnesses.
- POS: author `<L>/zcode`, witnesses `human/operator` and `xai/grok-4.7`. These are three lineages, all pairwise distinct (valid only if L != xai; see section 2, step 0).

**Pair C (keys are not lineage)**
- NEG: grok-4.7 called twice through two different xAI keys, posted as `xai/grok-a` and `xai/grok-b`. This is one lineage, so it counts as one witness.
- POS: grok-4.7 through one key, plus the operator. This is two lineages.

**Pair D (the echo)**
- NEG: a different-lineage mate given the author's full session transcript and asked to "confirm". F1 holds but F3 fails, so it is not a witness.
- POS: the same mate given only the packet in section 2, with the instruction to return AGREE, DISAGREE, or CANNOT-TELL.

**Pair E (transport is not substrate)**
- NEG: an MCP bridge client that relays to the same backend family as the author. The bridge changes the pipe, not the mind, so it has the author's lineage.
- POS: an MCP bridge client whose backend family is declared and differs from the author's and from the other witness's.

---

## (2) Bootstrap design (7 days, existing machinery only)

### Binding: what the witness signs

**Honest naming first.** No seat holds a signing key the ledger verifies, and the xAI API returns response ids, not vendor signatures (UNVERIFIED for grok-4.7 specifically). The protocol therefore uses a **commitment chain**, not a signature.

1. The target claim row carries G2 `src_sha256_12` over its evidence (C5) and a G3 warrant (C6). Its chain hash, the 12-hex row hash, commits to the claim bytes. That the row hash covers text, src hashes, and warrant is UNVERIFIED; confirm in the row-hash function before step 2.
2. Each witness receives packet P:
   ```
   estate-witness.v0
   target_row_hash: <12hex>
   claim_text_sha256: <sha256 of the claim text bytes exactly as stored in the row>
   evidence: <path> <src_sha256_12>   (one line per bound source)
   warrant: <command> expect_exit=0
   witness_seat: <lineage>/<instance>
   context: packet-only
   verdict: AGREE | DISAGREE | CANNOT-TELL
   reason: <one line, must name a line of the evidence>
   ```
3. A machine witness must echo `target_row_hash` and `claim_text_sha256` verbatim in its response. A mismatched or missing echo voids its packet.
4. The raw response is saved as an evidence file and posted as its own G2-bound claim by the witness seat. Any later edit then becomes a standing verify FAIL via `_evidence_mutated` (C5).
5. The `witness` verb is run against `target_row_hash` with seat `<lineage>/<instance>`. It executes g1/g2/g3 locally (C4), and the row is chained by `prev`.

What this proves: the judgment bytes and the claim bytes are mutually bound and tamper-evident from step 4 onward.

What it does NOT prove: that the named lineage produced the judgment. A local driver could fabricate the JSON. Section 3 covers this.

### Protocol

**Step 0 (day 1). Preconditions.**
- Re-run M1 and record the counts.
- Determine the author's lineage L. The evidence does not state zcode's vendor (UNVERIFIED).
- Pick witness 1 = `human/operator`.
- Pick witness 2 = `xai/grok-4.7` if L != xai. Otherwise pick a local mate of a third lineage.

**Step 1 (day 1). Land section 4 and verify the null effect.**
- Land the one-line change through the normal pre-push hook.
- Re-run verify. Expect identical counts with `0 corroborated`. Any changed count blocks the protocol.

**Step 2 (day 2). Post the target claim as `<L>/zcode`.**
- **Claim:** "tools/workflow_gate.py check --scenarios configs/workflow_gate_scenarios exits 0 with 7 cards validated, on the bound bytes."
- **G2 sources:** tools/workflow_gate.py and the scenario cards.
- **G3 warrant:** `.venv/Scripts/python.exe tools/workflow_gate.py check --scenarios configs/workflow_gate_scenarios`.
- **Why this claim:** it is read-only and deterministic, and it already exited 0 in the ractor50 lane. That run is recorded in logic.md "Checks run by the lane" item 1. Its moment is the gala_20260925 lane, its instrument the venv python.
- **Unknowns:** the exact post CLI flags are UNVERIFIED. Read the post() signature near C2 before running.

**Step 3 (day 3). Witness 2 (grok).**
- Send P with the verdict line blank, in a fresh API session with no prior estate context.
- Save the response JSON to `watch/inbox/witness/<target_row_hash>_xai.json` and post it per binding step 4.
- Only if the verdict is AGREE and the echo matches, run `witness` as `xai/grok-4.7`.

**Step 4 (day 4). Witness 1 (operator).**
- The operator receives P only, runs the warrant by hand, and reads the evidence line named in their reason.
- The operator does not open grok's response first.
- Post the operator's packet text as a G2-bound claim, then run `witness` as `human/operator`.

**Step 5 (day 4-5). Read the result.**
- Run verify. The success read is `ADMISSION: 1 corroborated`.
- Record instrument, moment (UTC), and the full ADMISSION line in a watch/inbox receipt.

**Days 6-7. Buffer and audit.**
- Use the time to retry if any check returned g2 != True or g3_exit != 0.
- Optionally have a third-lineage context-blind mate recompute and post a non-counting AGREE or DISAGREE as an audit sample.

### Negative example of the protocol

Operator and grok both see each other's verdicts before posting, and both rows land within 2 minutes. This satisfies the line in section 4 but violates F3. Treat it as void-eligible, not as the bootstrap row.

---

## (3) Anti-collusion (the republic of puppets)

**Verdict: preventable only against honest mistakes and casual seat renaming; against a deliberate single-owner fabricator it is detectable at best, and only probabilistically.**

### What the rule prevents

- Same-family seat farms (zcode, zcode-2, zcode-desk) can no longer corroborate each other. Lineage collapses them.
- Unprefixed legacy seats cannot contribute at all.
- Unprefixed authors cannot reach the rung, so there is no unknown-lineage author for a witness to differ from by default.

### What it cannot prevent

Because of C2, anyone with write access can post `xai/grok-4.7` without calling xAI, or append directly to the file. 13 unattributed rows already did the latter (M1). One owner holds every key, so no cryptographic step inside the estate can distinguish a real second mind from a puppet.

### Detectors (all existing machinery or reads)

| Detector | What it does | Strength |
|---|---|---|
| D1 Transcript presence | A machine-lineage witness row without a G2-bound response file naming its `target_row_hash` is void-eligible under FORGED (C7). | Mechanical check |
| D2 Vendor-side cross-check | The response id in the saved JSON is checked against the funded xAI account's usage records, if that console exposes per-request ids (UNVERIFIED). This is the only check anchored outside the owner's filesystem. | Strongest available |
| D3 Batch timing | Flag any corroboration whose two witness rows land within 10 minutes of each other. The precedent is all 10 cross-signature rows in one 6-minute window (w4-trust-game receipt 3). | Heuristic |
| D4 Unanimity | A real two-lineage panel produces DISAGREE or CANNOT-TELL sometimes. Zero non-AGREE verdicts over 20 or more packets is a puppet signal. | Heuristic |
| D5 Stranger audit | When the planned stranger test runs, have the stranger re-witness a random sample of CORROBORATED rows. Disagreement above the panel's own disagreement rate indicts the republic. This is the only detector carrying the economic axis. | Strongest in principle, not yet available |

---

## (4) Migration

Current rule, as carried by the receipt at mag/grounding_wave.py:325-335 (C1, RQ): `len(seats) >= 2`.

Replace that expression with:

```python
"/" in author and len({s.split("/", 1)[0] for s in seats if "/" in s} - {author.split("/", 1)[0]}) >= 2
```

Before applying:
- The names `seats` and `author` being in scope at that line is UNVERIFIED. The applying seat must confirm them at :325-335 and rename to match.
- The neighbouring conditions (not-author, all checks passing) and SELF_SIGNED (C3) stay unchanged.

Effect: corroboration counts distinct lineage prefixes, excluding the author's lineage. Unprefixed seats are ignored, and unprefixed authors cannot corroborate. Convention: seat = `<lineage>/<instance>`.

---

## (5) Falsifier

The rib is wrong, and should be reverted or amended, if any of the following holds:

1. **The independence claim fails (core falsifier).**
   - **Setup:** run 10 off-ledger canary packets, 5 true and 5 planted-false (evidence line contradicts claim text). Do not post them; this keeps the tape clean.
   - **Panels:** a lineage-distinct pair (operator + grok) and a same-lineage pair (two zcode-family instances), all context-blind.
   - **Falsified if:** the distinct pair co-AGREEs on planted-false packets at a rate not lower than the same-lineage pair. Lineage is then not the axis of error independence, and section 1's definition fails.
   - **Record:** packet ids, verdicts, and UTC times per packet.
2. **The bootstrap fails.** By day 7, verify does not print `ADMISSION: 1 corroborated` (or higher) after steps 1-5 ran with g2=True and g3_exit=0 on both witness rows.
3. **The migration is not a null change.** Verify at step 1 shows any count different from the M1 re-run taken at step 0, both under the same instrument and the same context.
4. **The gate leaks.** Corroborated rises above 0 while any counted witness row carries an unprefixed seat, the author's lineage, or no D1 transcript. This is the logic.md law 3 falsifier, sharpened from seat to lineage.
